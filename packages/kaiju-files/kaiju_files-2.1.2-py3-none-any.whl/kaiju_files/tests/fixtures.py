import pytest

from kaiju_files.services import FileService, FileConverterService

__all__ = ['files_dir', 'file_service', 'file_converter_service']


@pytest.fixture()
def files_dir(tmp_path):
    yield tmp_path / '_files'


@pytest.fixture
def file_service(app, database_service, files_dir) -> FileService:
    service = FileService(app, database_service=database_service, dir=files_dir)
    app.services.add_service(service)
    return service


@pytest.fixture
def file_converter_service(app, database_service, file_service) -> FileConverterService:
    service = FileConverterService(app, database_service=database_service, file_service=file_service)
    app.services.add_service(service)
    return service


# @pytest.fixture
# def sample_file():
#     def _file(content: bytes):
#         f = NamedTemporaryFile(prefix='pytest', delete=False, mode='wb')
#         f.write(content)
#         f.close()
#         p = Path(f.name)
#         return p
#
#     yield _file
