import io
from typing import BinaryIO, AsyncGenerator, Iterable
from contextlib import asynccontextmanager

from botocore.exceptions import UnknownKeyError
from botocore.client import BaseClient
import aioboto3

from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol


class MinioFilesStorage(FilesStorageProtocol):
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
    ):
        self.config = dict(
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[BaseClient, None]:
        session = aioboto3.Session()
        async with session.client("s3", **self.config) as client:
            yield client

    async def save(self, category: str, filename: str, content: BinaryIO) -> str:
        async with self._get_client() as client:
            # Если бакета нет - создаём
            existing = await client.list_buckets()
            bucket_names: Iterable[str] = (bucket["Name"] for bucket in existing["Buckets"])
            if category not in bucket_names:
                await client.create_bucket(Bucket=category)

            await client.upload_fileobj(content, category, filename)

        return filename

    async def get(
            self, category: str, filename: str
    ) -> BinaryIO:
        async with self._get_client() as client:
            response = await client.get_object(
                Bucket=category,
                Key=filename,
            )
            body = await response["Body"].read()  # Считываем как байты
            return io.BytesIO(body)

    async def delete(self, category: str, filename: str) -> bool:
        async with self._get_client() as client:
            try:
                await client.delete_object(
                    Bucket=category,
                    Key=filename,
                )
                return True
            except UnknownKeyError:
                return False
