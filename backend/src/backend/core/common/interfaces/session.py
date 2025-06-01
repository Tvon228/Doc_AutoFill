from abc import abstractmethod
from typing import Any, Protocol


class SessionProtocol(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self, objects: Any) -> None:
        raise NotImplementedError
