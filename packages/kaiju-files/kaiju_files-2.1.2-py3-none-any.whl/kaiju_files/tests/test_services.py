import tempfile
import uuid
from typing import Generator, Tuple

import pytest
import pytest_asyncio

from kaiju_db.tests.test_db import TestSQLService

from kaiju_files.types import AbstractFileConverter
from kaiju_files.services import FileService, File, FileConverterService, Converter, CONVERTERS

__all__ = ['TestFileService', 'TestFileConverterService']


@pytest.mark.docker
@pytest.mark.asyncio
class TestFileService(TestSQLService):
    """Test file service."""

    table_names = [FileService.table.name]

    @staticmethod
    def get_rows(num: int) -> Generator[File, None, None]:
        for n in range(num):
            yield File(id=uuid.uuid4(), hash=uuid.UUID(int=1), name=f'test_file_{n}', extension='txt', meta={})

    @pytest.fixture
    def _service(self, file_service):
        return file_service

    @staticmethod
    def update_value() -> dict:
        return {'hash': uuid.UUID(int=2)}

    @staticmethod
    def update_condition() -> dict:
        return {'hash': uuid.UUID(int=1)}

    @staticmethod
    def check_update(row: dict) -> bool:
        return row['hash'] == uuid.UUID(int=2)


@pytest.mark.docker
@pytest.mark.asyncio
class TestFileConverterService(TestSQLService):
    """Test file converters service."""

    table_names = [FileConverterService.table.name]

    class _UppercaseConverter(AbstractFileConverter):
        def _convert(self, input_buffer, **metadata) -> Generator[Tuple[tempfile.NamedTemporaryFile, dict], None, None]:
            output_file = self._create_file()
            output_file.write(input_buffer.read().upper())
            yield output_file, metadata

    @classmethod
    def get_rows(cls, num: int) -> Generator[Converter, None, None]:
        for n in range(num):
            yield Converter(
                id=uuid.uuid4(),
                cls=cls._UppercaseConverter.__name__,
                name=f'test_converter_{n}',
                system=True,
                settings={},
            )

    @pytest.fixture
    def _service(self, app, file_service, file_converter_service):
        CONVERTERS.register(self._UppercaseConverter)
        return file_converter_service

    @pytest_asyncio.fixture
    async def _test_file(self, file_service, files_dir):
        name = uuid.uuid4().hex
        new_file = next(TestFileService.get_rows(1))
        await file_service.create(new_file)
        file_path = files_dir / name
        with open(files_dir / name, 'w') as f:
            f.write(name.lower())
        await file_service.upload_local_file(new_file['id'], file_path)
        yield new_file

    async def test_file_conversion(self, _store: FileConverterService, _test_file, _row):
        await _store.create(_row)
        result = await _store.convert(_row['id'], _test_file['id'])
        _store.logger.debug(result)

    @staticmethod
    def update_value() -> dict:
        return {'system': False}

    @staticmethod
    def update_condition() -> dict:
        return {'system': True}

    @staticmethod
    def check_update(row: dict) -> bool:
        return row['system'] is False
