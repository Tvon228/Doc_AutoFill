from typing import Protocol, BinaryIO


class FilesStorageProtocol(Protocol):
    async def save(
            self, category: str, filename: str, content: BinaryIO
    ) -> str: ...

    async def get(
            self, category: str, filename: str
    ) -> BinaryIO: ...

    async def delete(self, category: str, filename: str) -> bool: ...
