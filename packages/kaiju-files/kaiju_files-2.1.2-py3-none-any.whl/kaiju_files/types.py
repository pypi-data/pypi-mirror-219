import abc
import re
import string
import tempfile
from pathlib import Path
from typing import *

import kaiju_tools.jsonschema as schema
from kaiju_tools.encoding import Serializable
from kaiju_tools.services import Service

__all__ = (
    'AbstractFileTransportInterface',
    'AbstractFileLoader',
    'AbstractFileConverter',
    'FileOperationConfigurationError',
)


class AbstractFileTransportInterface(abc.ABC):
    """Connector to an external file storage."""

    @abc.abstractmethod
    async def has_new_files(self) -> bool:
        """Return True if new downloadable files found in shared folders."""

    @abc.abstractmethod
    async def list(self) -> AsyncGenerator[Path, None]:
        """List all files in shared folders."""

    @abc.abstractmethod
    async def download(self, uri: Path) -> tempfile.NamedTemporaryFile:
        """Download a file to a local temp dir and return the location."""

    @abc.abstractmethod
    async def delete(self, uri: Path):
        """Remove a downloaded file from a shared directory."""

    @abc.abstractmethod
    async def mark_failed(self, uri: Path, reason: str, message: str = ''):
        """Mark a shared file as failed and (optionally) move it to another shared location."""


class FileOperationConfigurationError(ValueError):
    """An error due to invalid file converter settings."""


class AbstractFileOperation(Service, abc.ABC):
    class Settings(Serializable):
        """Settings object for a file operation class.

        Inner class because it's not to be used apart from its parent converter.
        """

        _strip_set = string.punctuation + string.whitespace

        __slots__ = ('filename_mask', 'directory_mask', 'ext', 'meta', 'output_extension')

        def __init__(
            self,
            filename_mask: str = None,
            directory_mask: str = None,
            ext: List[str] = None,
            meta: dict = None,
            output_extension: str = None,
        ):
            """Initialize.

            :param filename_mask: regular expression mask for input filenames,
                named groups are allowed and will be used for extracting
                file metadata if needed, None (default) for no specific mask
            :param directory_mask: same as filename mask but for parent dir
            :param ext: list of allowed file extensions, only alphanumeric
                chars allowed, None (default) for no specific extensions
            :param meta: specific metadata added to converted files
            :param output_extension: output file extension
            """
            try:
                self.filename_mask = re.compile(filename_mask) if filename_mask else None
            except re.error:
                raise FileOperationConfigurationError(
                    'Invalid filename mask "%s". Must be None or' ' a valid regular expression.' % filename_mask
                )

            try:
                self.directory_mask = re.compile(directory_mask) if directory_mask else None
            except re.error:
                raise FileOperationConfigurationError(
                    'Invalid directory mask "%s". Must be None or' ' a valid regular expression.' % directory_mask
                )

            if ext is None:
                ext = []
            if isinstance(ext, Iterable):
                self.ext = []
                for e in ext:
                    e = str(e).strip(self._strip_set).lower()
                    if e:
                        self.ext.append(e)
                if self.ext:
                    self.ext = frozenset(self.ext)
                else:
                    self.ext = None
            else:
                raise FileOperationConfigurationError('Invalid extension set "%s". Must be an iterable object' % ext)
            self.meta = dict(meta) if meta else {}
            self.output_extension = output_extension

        def match(self, uri: Path) -> Optional[dict]:
            """Match a filename using an `input_mask`.

            The resulting data will be returned in a group dict. In case of no match the dict will be empty.
            """
            groups = {}

            if self.ext:
                ext = uri.suffix.lower().lstrip('.')
                if ext in self.ext:
                    groups['extension'] = ext
                else:
                    return None

            if self.filename_mask:
                match = self.filename_mask.fullmatch(str(uri.stem))
                if match:
                    groups.update(match.groupdict())
                else:
                    return None

            if self.directory_mask:
                match = self.filename_mask.fullmatch(str(uri.parent))
                if match:
                    groups.update(match.groupdict())
                else:
                    return None

            groups['uri'] = str(uri)
            return groups

        def repr(self) -> dict:
            return {
                'filename_mask': self.filename_mask.pattern if self.filename_mask else None,
                'directory_mask': self.directory_mask.pattern if self.directory_mask else None,
                'ext': list(self.ext) if self.ext else None,
                'meta': self.meta,
                'output_extension': self.output_extension,
            }

        @classmethod
        def spec(cls) -> schema.Object:
            return schema.Object(
                filename_mask=schema.Nullable(
                    schema.String(
                        title='Regex mask for matching a file name.',
                        description='All groups will be written to "meta" dict of a file.'
                        ' If no match, the file counts as rejected.'
                        ' If mask is "null", then all filenames are accepted.',
                        format='regex',
                        minLength=1,
                    )
                ),
                directory_mask=schema.Nullable(
                    schema.String(
                        title='Regex mask for matching a file directory name.',
                        description='All groups will be written to "meta" dict of a file.'
                        ' If no match, the file counts as rejected.'
                        ' If mask is "null", then all filenames are accepted.',
                        format='regex',
                        minLength=1,
                    )
                ),
                ext=schema.Nullable(
                    schema.Array(
                        title='A list of allowed file extensions.',
                        description='If it is "null", then all extensions are accepted.',
                        items=schema.String(minLength=1),
                        uniqueItems=True,
                        minItems=1,
                    )
                ),
                meta=schema.Nullable(schema.Object(title='Optional file metadata, will be written to a file.')),
                output_extension=schema.Nullable(
                    schema.String(
                        title='An output file extension.',
                        description='If it is "null", then an original extension will be used.',
                        minLength=1,
                    )
                ),
                title='File operation class settings.',
                additionalProperties=False,
            )

    def __init__(self, *args, settings: Union[dict, List[dict]] = None, **kws):
        """Initialize.

        :param settings: converter specific settings
        """
        super().__init__(*args, **kws)
        self.settings = self.Settings(**settings)

    @classmethod
    def spec(cls):
        return schema.Object(settings=cls.Settings.spec())

    def match(self, uri: Path) -> Optional[dict]:
        """Match a filename using an `input_mask`.

        The resulting data will be returned in a group dict. In case of no match the dict will be empty.
        """
        return self.settings.match(uri)


class AbstractFileLoader(AbstractFileOperation, abc.ABC):
    """File uploading and metadata interface."""

    class Settings(AbstractFileOperation.Settings):
        """File loader settings."""

    @abc.abstractmethod
    async def upload(self, data: tempfile.NamedTemporaryFile, **metadata):
        """Upload a file from local temp dir and sets its metadata."""


class AbstractFileConverter(AbstractFileOperation, abc.ABC):
    """File converter/normalizer which is supposed to be run in a thread / process."""

    class Settings(AbstractFileOperation.Settings):
        """File converter settings."""

    READ_MODE = 'rb'
    WRITE_MODE = 'wb'
    MAX_PROCESSING_TIME = 300

    def __init__(
        self,
        *args,
        dir: str = '.',
        read_mode=READ_MODE,
        write_mode=WRITE_MODE,
        max_processing_time=MAX_PROCESSING_TIME,
        settings: Union[dict, List[dict]] = None,
        **kws,
    ):
        """Initialize.

        :param dir: path to a temp local data storage
        :param read_mode: read mode for opening original files
        :param write_mode: write mode for writing new (converted) files
        :param max_processing_time: maximum file processing time in seconds
        :param settings: converter specific settings
        """
        super().__init__(*args, settings=settings, **kws)
        self._dir = Path(dir).resolve()
        self.max_processing_time = max(1, int(max_processing_time))
        self._read_mode = read_mode
        self._write_mode = write_mode
        self._files = []

    def convert(
        self, file: Union[Path, str, tempfile.NamedTemporaryFile], return_exceptions=False, **metadata
    ) -> List[Tuple[tempfile.NamedTemporaryFile, dict]]:
        """Call a converter and returns created file paths and metadata."""

        def _process_file(_input_buffer):
            data = self._convert(_input_buffer, **metadata)
            for _t_file, _metadata in data:
                if not _t_file.closed:
                    _t_file.close()
                version_metadata = {}
                version_metadata.update(metadata)
                version_metadata.update(self.settings.meta)
                version_metadata.update(_metadata)
                files.append((_t_file, version_metadata))

        try:
            files = []
            try:
                if isinstance(file, (Path, str)):
                    with open(str(file), mode=self._read_mode) as input_buffer:
                        _process_file(input_buffer)
                else:
                    with open(file.name, mode=self._read_mode) as input_buffer:
                        _process_file(input_buffer)
            except Exception as err:
                if return_exceptions:
                    files = err
                else:
                    raise
        finally:
            for t_file in self._files:
                if not t_file.closed:
                    t_file.close()
            self._files = []

        return files

    @abc.abstractmethod
    def _convert(self, input_buffer, **metadata) -> Generator[Tuple[tempfile.NamedTemporaryFile, dict], None, None]:
        """Convert files.

        You must define your custom file processing method here.
        This method should yield your new files aside with its meta-information.

        :param input_buffer: opened source file buffer passed automatically
        :param metadata: additional meta-information
        """
        output_file = self._create_file()
        with output_file.open(self._write_mode):
            """Do here what you need and return your
            output file path and additional data."""
        yield output_file, metadata

    def _create_file(self, ext=None, dir=None):
        """Create new files."""
        if ext:
            ext = f'.{ext}'
        if dir is None:
            dir = self._dir
        else:
            dir = str(dir)
        t_file = tempfile.NamedTemporaryFile(
            dir=dir, mode=self._write_mode, delete=False, prefix=f'{self.__class__.__name__}_', suffix=ext
        )
        self._files.append(t_file)
        return t_file
