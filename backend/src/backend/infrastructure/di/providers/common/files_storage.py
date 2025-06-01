from dishka import provide, Scope, Provider, from_context

from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol
from src.backend.infrastructure.adapters.files_storage import MinioFilesStorage
from src.backend.main.config import MinioConfig


class FilesStorageProvider(Provider):
    scope = Scope.REQUEST

    config: MinioConfig = from_context(provides=MinioConfig, scope=Scope.APP)

    @provide
    async def provide_files_storage(self, config: MinioConfig) -> FilesStorageProtocol:
        return MinioFilesStorage(
            endpoint_url=config.endpoint_url,
            access_key=config.access_key,
            secret_key=config.secret_key
        )
