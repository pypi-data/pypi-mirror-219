import hashlib
import os
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile, TemporaryFile
from typing import Union, Optional, TypedDict, List, cast, Type, Tuple

import aiofiles
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

from kaiju_tools.app import SERVICE_CLASS_REGISTRY, ContextableService
from kaiju_tools.exceptions import NotFound, ValidationError
from kaiju_tools.functions import async_run_in_thread
from kaiju_tools.interfaces import PublicInterface
from kaiju_tools.registry import ClassRegistry
from kaiju_tools.mapping import recursive_update
from kaiju_db import SQLService, DatabaseService

from kaiju_files.types import AbstractFileConverter

__all__ = ['FileService', 'FileConverterService', 'FileConvertersRegistry', 'CONVERTERS', 'Converter', 'File']


class FileConvertersRegistry(ClassRegistry[str, Type[AbstractFileConverter]]):
    """Registry of all file converters."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (AbstractFileConverter,)


CONVERTERS = FileConvertersRegistry()


class Converter(TypedDict, total=False):
    """File converter data."""

    id: uuid.UUID
    cls: str
    name: str
    system: bool
    settings: dict
    timestamp: datetime


class _ConvertedVersionInfo(TypedDict):
    name: str
    extension: str
    meta: dict


class _ConvertedFileInfo(TypedDict):
    file_id: uuid.UUID
    converter_id: uuid.UUID
    versions: List[_ConvertedVersionInfo]


class FileConverterService(SQLService[uuid.UUID, Converter], PublicInterface):
    """File converters storage and execution.

    You can use it for image and other data types conversion.

    First if you need a specific converter class you should inherit it from `AbstractFileConverter`
    interface and register it in `converters` class registry.

    .. code-block:: python

        from kaiju_files.abc import AbstractFileConverter
        from kaiju_files.converters import converters

        class MyConverterClass(AbstractFileConverter):
            ...

        converters.register_class(MyConverterClass)


    You can use it in you converter service. It's best to init this service within a
    service context manager, but you can create it directly by providing instances of a database
    service and a file service. Then you can save your converter settings and convert files
    using your converter.

    .. code-block:: python

        my_converter_settings = {...}

        async with FileConverterService(...) as fcs:
            row = {'cls': 'MyConverterClass', 'name': 'my converter', 'settings': my_converter_settings}
            row = await fcs.create(row)
            versions_info = await fsc.convert(row['id'], my_file_id)

    """

    class ErrorCode:
        """Converter error codes."""

        NO_CONVERTER_CLASS_FOUND = 'NO_CONVERTER_CLASS_FOUND'
        INVALID_CONVERTER_SETTINGS = 'INVALID_CONVERTER_SETTINGS'

    table = sa.Table(
        'converters',
        sa.MetaData(),
        sa.Column('id', sa_pg.UUID, nullable=False, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('cls', sa_pg.VARCHAR, nullable=False),
        sa.Column('name', sa_pg.TEXT, nullable=False, unique=True),
        sa.Column('system', sa_pg.BOOLEAN, nullable=False, default=False),
        sa.Column('settings', sa_pg.JSONB, nullable=False),
        sa.Column(
            'timestamp',
            sa_pg.TIMESTAMP,
            nullable=False,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp()),
        ),
    )

    def __init__(
        self,
        app,
        database_service: DatabaseService,
        file_service: 'FileService' = False,
        converters: FileConvertersRegistry = CONVERTERS,
        max_processing_time: int = 300,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param database_service:
        :param file_service:
        :param converters: converters registry (uses default registry)
        :param max_processing_time: conversion time limit (sec)
        :param logger:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        self.file_service = self.discover_service(file_service)
        self.converters = converters
        self.max_processing_time = max(1, int(max_processing_time))

    @property
    def routes(self) -> dict:
        return {**super().routes, 'classes': self.get_converter_class_specs, 'call': self.convert}

    async def get_converter_class_specs(self, cls: str = None):
        """Return a list of registered converter classes specification."""
        if cls:
            _cls = self._get_converter_class(cls)
            return {'cls': cls, 'spec': _cls.spec()}
        else:
            return [{'cls': cls, 'spec': _cls.spec()} for cls, _cls in self.converters.items()]

    async def convert(self, id, file_id, settings: dict = None, metadata: dict = None, **__) -> _ConvertedFileInfo:
        """Convert a file.

        :param id: converter ID
        :param file_id: file to convert
        :param settings: additional converter settings
        :param metadata: additional metadata
        :return:
        """
        base_file_info = await self.file_service.get(file_id, columns=['name', 'extension', 'meta', 'hash'])
        base_meta = base_file_info['meta']

        if metadata is None:
            metadata = base_meta
        else:
            base_meta.update(metadata)
            metadata = base_meta

        file_path = self.file_service._get_local_file_path(base_file_info['hash'])
        if not file_path.exists():
            raise RuntimeError('Local file referenced by this id (%s) does not exist.' % file_id)
        converter = await self.init_converter(id, settings)
        kws = {**metadata, 'return_exceptions': True, 'max_exec_time': converter.max_processing_time}
        result = await async_run_in_thread(converter.convert, (file_path,), kws)
        data = []

        if isinstance(result, Exception):
            raise result

        for f, meta in result:
            version_name = meta.get('version')
            if not version_name:
                version_name = self.converters.get_key(type(converter))
            output_ext = meta.get('output_extension')
            if not output_ext:
                output_ext = base_file_info['extension']
            name = meta.get('name')
            if not name:
                name = base_file_info['name']
            name = f'{name}__{version_name}'
            version = {'name': name, 'extension': output_ext, 'meta': meta}
            file_info = await self.file_service.create(version)
            try:
                file_info = await self.file_service.upload_local_file(file_info['id'], f.name)
            except Exception:
                await self.file_service.delete_local_file(f.name)
                raise
            else:
                version['file'] = file_info
                data.append(version)

        return {'file_id': file_id, 'converter_id': id, 'versions': data}  # noqa

    def prepare_insert_data(self, data: dict) -> Converter:
        cls, settings = data['cls'], data.get('settings', {})
        converter = self._create_converter(cls, settings)
        data['settings'] = converter.settings.repr()
        return data

    def _get_converter_class(self, cls: str) -> Type[AbstractFileConverter]:
        if cls not in self.converters:
            keys = self.converters.keys()
            raise NotFound(
                'Converter class does not exist.',
                key=cls,
                available_classes=list(keys),
                code=self.ErrorCode.NO_CONVERTER_CLASS_FOUND,
            )
        return cast(Type[AbstractFileConverter], self.converters[cls])

    async def init_converter(self, id, settings=None) -> AbstractFileConverter:
        """Return a converter instance ready to use.

        :param id: converter ID
        :param settings: additional settings to update default settings
        """
        converter = await self.get(id, columns='*')
        if settings:
            settings = recursive_update(converter['settings'], settings)
        else:
            settings = converter['settings']
        converter = self._create_converter(converter['cls'], settings)
        if isinstance(converter, ContextableService):
            await converter.init()
        return converter

    def _create_converter(self, cls: str, settings: dict) -> AbstractFileConverter:
        """Create a new converter object from a class name and settings dict.

        :param cls: class name as in converters registry (uses `class.__name__` by default)
        """
        cls = self._get_converter_class(cls)
        try:
            converter = cls(
                app=self.app,
                dir=self.file_service.temp_dir,
                settings=settings,
                max_processing_time=self.max_processing_time,
                logger=self.logger,
            )
        except (ValueError, AttributeError, TypeError) as e:
            raise ValidationError(str(e), base_exc=e, converter_cls=cls, code=self.ErrorCode.INVALID_CONVERTER_SETTINGS)
        else:
            return converter


class File(TypedDict, total=False):
    """File data."""

    id: uuid.UUID
    hash: Optional[uuid.UUID]
    name: Optional[str]
    extension: Optional[str]
    timestamp: datetime
    meta: dict


class FileService(SQLService[uuid.UUID, File], ContextableService, PublicInterface):
    """File management service which handlers uploads and downloads.

    It's expected to be initialized within a service context manager, but it's possible to do
    initialization manually by directly providing an instance of the database service.

    File service consists of two main parts: file records table and actual files stored in a local
    directory.

    To upload a file first you have to create an empty file record with all metadata about the file
    and then link it to a local file or upload data referencing the record by its id.

    .. code-block:: python

        async with FileService(app, database_service):
            data = await file_service.create({'name': 'test', 'extension': 'txt', 'meta': {'tag': 'file'}})
            data = await file_service.upload_local_file(data['id'], file_path)

    Files are stored locally under their hash UUID and symlinked using their specified names, thus
    same files with different names can coexist in a filesystem and may be served statically via nginx
    or other server.
    """

    service_name = 'files'
    DELETE_UNLINKED_INTERVAL_DAYS = 1

    table = sa.Table(
        'files',
        sa.MetaData(),
        sa.Column('id', sa_pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('hash', sa_pg.UUID, nullable=True),
        sa.Column('name', sa_pg.TEXT, nullable=True),
        sa.Column('extension', sa_pg.TEXT, nullable=True),
        sa.Column(
            'timestamp',
            sa_pg.TIMESTAMP,
            nullable=False,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp()),
        ),
        sa.Column('meta', sa_pg.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Index('idx__files__hash', 'hash', postgresql_using='hash'),
        sa.Index('idx__files__ext', 'extension', postgresql_using='hash'),
        sa.Index('idx__files__name', 'name', postgresql_using='hash'),
        sa.Index('idx__files__timestamp', 'timestamp', postgresql_using='btree', postgresql_ops={'timestamp': 'DESC'}),
    )

    def __init__(
        self,
        app,
        database_service: DatabaseService,
        dir: str = '.',
        uri_prefix: str = '/files/',
        logger=None,
    ):
        """Initialize.

        :param app:
        :param database_service:
        :param dir: local file storage path
        :param uri_prefix: optional prefix for returned URIs
        :param logger:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        self._dir = Path(dir).resolve()
        self._dir.mkdir(exist_ok=True, parents=True)
        self._uri_prefix = Path(uri_prefix)
        self._temp_dir = None
        self.virtual_columns = {'uri': f"'{self._uri_prefix}' || '/' || hash || '/' || name || '.' || extension"}

    @property
    def routes(self) -> dict:
        routes = {**super().routes, 'delete_unlinked': self.delete_unlinked_files}
        return routes

    @property
    def permissions(self) -> dict:
        return {self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_USER_PERMISSION}

    async def init(self):
        self._temp_dir = TemporaryDirectory(prefix='FileService')
        self._temp_dir.__enter__()

    async def close(self):
        if not self.closed:
            self._temp_dir.__exit__(None, None, None)
            self._temp_dir = None

    @property
    def closed(self) -> bool:
        return self._temp_dir is None

    @property
    def temp_dir(self) -> Path:
        return Path(self._temp_dir.name)

    async def upload_local_file(self, id: uuid.UUID, path: Union[str, Path, NamedTemporaryFile], move=True):
        """Upload local file.

        Use this method to 'upload' a local file. This operation will move the file into a file service
        directory and link it to a file record.

        :param id: file record id
        :param path: local file path
        :param move: move file instead of copying it
        :return: file and URI
        """
        data = await self.get(id, columns=['name', 'extension', 'meta'])
        _hash = hashlib.md5()
        temp_file = self.get_temp_file_path()
        temp_file.parent.mkdir(exist_ok=True, parents=True)

        if isinstance(path, str):
            pass
        elif isinstance(path, Path):
            path = str(path)
        else:
            path = path.name

        async with aiofiles.open(path, 'rb') as _f:
            size = 1024**2
            chunk = await _f.read(size)
            while chunk:
                _hash.update(chunk)
                chunk = await _f.read(size)

        _hash = uuid.UUID(_hash.hexdigest())
        id, uri = await self._upload(
            file_id=id,
            path=path,
            hash=_hash,
            name=data['name'],
            extension=data['extension'],
            meta=data['meta'],
            _move=move,
        )

        return {'id': id, 'uri': str(uri)}

    async def upload_content(self, id: uuid.UUID, content, _move=True):
        data = await self.get(id, columns=['name', 'extension', 'meta'])
        hash = hashlib.md5()
        temp_file = self.get_temp_file_path()
        temp_file.parent.mkdir(exist_ok=True, parents=True)

        async with aiofiles.open(temp_file, 'wb') as _f:
            async for chunk in content.iter_chunked(1024**2):
                hash.update(chunk)
                await _f.write(chunk)

        hash = uuid.UUID(hash.hexdigest())
        id, uri = await self._upload(
            file_id=id,
            path=temp_file,
            hash=hash,
            name=data['name'],
            extension=data['extension'],
            meta=data['meta'],
            _move=_move,
        )

        return {'id': id, 'uri': str(uri), 'hash': hash, 'tmp_file': temp_file}

    async def delete_unlinked_files(self, days=DELETE_UNLINKED_INTERVAL_DAYS):
        """Remove all old file record which have no hash (i.e. an actual file) linked to them."""
        t = datetime.now() - timedelta(days=days)
        sql = self.table.delete().where(sa.and_(self.table.c.hash == None, self.table.c.timestamp < t))  # noqa alchemy
        await super()._wrap_delete(None, self._db.execute(sql))

    @staticmethod
    async def delete_local_file(name: Union[Path, str, TemporaryFile]):
        if isinstance(name, str):
            pass
        elif isinstance(name, Path):
            name = str(name)
        else:
            name = name.name
        path = Path(name)
        if path.exists():
            await async_run_in_thread(os.unlink, args=(name,))

    async def get_local_file_path(self, id: uuid.UUID):
        file_info = await self.get(id=id, columns=['hash'])
        path = self._get_local_file_path(file_info['hash'])
        return path

    def _get_local_file_path(self, hash: Optional[uuid.UUID]) -> Optional[Path]:
        if hash:
            return self._dir / str(hash) / str(hash)

    @staticmethod
    def _get_local_file_name(name: Optional[str], hash: Optional[uuid.UUID], extension: Optional[str]) -> Optional[str]:
        if extension:
            return f'{name}.{extension}'
        elif name:
            return f'{name}'
        elif hash:
            return str(hash)

    def _get_file_uri(self, name: Optional[str], hash: Optional[uuid.UUID], extension: Optional[str]) -> Optional[Path]:
        name = self._get_local_file_name(name=name, hash=hash, extension=extension)
        if name:
            return self._uri_prefix / str(hash) / name

    def _get_local_symlink_path(
        self, name: Optional[str], extension: Optional[str], hash: Optional[uuid.UUID]
    ) -> Optional[Path]:
        name = self._get_local_file_name(name=name, extension=extension, hash=hash)
        if name:
            return self._dir / str(hash) / name

    def get_temp_file_path(self) -> Path:
        temp_file_name = str(uuid.uuid4())
        return self.temp_dir / temp_file_name

    async def get_temp_dir(self, *args, **kws) -> TemporaryDirectory:
        kws = {**kws, 'dir': self._temp_dir}
        _dir = await async_run_in_thread(TemporaryDirectory, args, kws)
        return _dir

    async def get_temp_file(self, *args, **kws) -> NamedTemporaryFile:
        kws = {**kws, 'dir': self._temp_dir}
        temp_file = await async_run_in_thread(NamedTemporaryFile, args, kws)
        return temp_file

    def get_temp_file_sync(self, *args, **kws) -> NamedTemporaryFile:
        temp_file = NamedTemporaryFile(*args, dir=self._temp_dir, **kws)
        return temp_file

    async def _delete_local_files(self, hash: Optional[uuid.UUID]):
        if hash:
            d = self._get_local_file_path(hash).parent
            if d.exists():
                await async_run_in_thread(shutil.rmtree, args=(str(d),))

    async def _upload(
        self,
        file_id: uuid.UUID,
        path: Union[Path, str],
        hash: uuid.UUID,
        name: str,
        extension: str,
        meta: dict,
        _move=True,
    ) -> (uuid.UUID, Path):
        file_path = self._get_local_file_path(hash)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        # uri = self._get_file_uri(name=name, hash=hash, extension=extension)
        if not file_path.exists():
            if _move:
                await async_run_in_thread(shutil.move, args=(str(path), str(file_path)))
            else:
                await async_run_in_thread(shutil.copy, args=(str(path), str(file_path)))
        else:
            await async_run_in_thread(os.unlink, args=(str(path),))
        link = self._get_local_symlink_path(name=name, hash=hash, extension=extension)

        if not link.exists():
            #     sql = self.table.select().with_only_columns([
            #         self.table.c.id
            #     ]).where(
            #         sa.and_(
            #             self.table.c.extension == extension,
            #             self.table.c.name == name,
            #             self.table.c.hash == hash
            #         )
            #     ).limit(1)
            #     data = await super()._wrap_get(self._db.fetchrow(sql))
            #     if data:
            #         await self.delete(file_id, columns=None)
            #         file_id = data['id']
            #         return file_id, uri
            # else:
            await async_run_in_thread(os.symlink, args=(str(file_path), str(link)))

        file_size = file_path.stat().st_size
        meta['file_size'] = file_size
        await self.update(id=file_id, data={'hash': hash, 'meta': meta}, columns=None)
        uri = self._get_file_uri(name=name, hash=hash, extension=extension)
        return file_id, uri

    @staticmethod
    def _create_file(name: str, extension: str = None, meta: dict = None):
        return {'name': name, 'extension': extension, 'meta': {} if meta is None else meta}

    def _insert_uri(self, data):
        data['uri'] = self._get_file_uri(name=data['name'], hash=data['hash'], extension=data['extension'])


SERVICE_CLASS_REGISTRY.register(FileService)
SERVICE_CLASS_REGISTRY.register(FileConverterService)
