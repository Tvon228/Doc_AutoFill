from abc import abstractmethod
from typing import Protocol

from src.backend.core.users.dto import AddUserDTO, UpdateUserDTO
from src.backend.core.users.entity import UserEntity


class UsersRepositoryProtocol(Protocol):

    @abstractmethod
    async def create(self, data: AddUserDTO, password_hash: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_by_id(self, ident: int) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> list[UserEntity] | None:
        ...

    @abstractmethod
    async def get_by_phone(self, phone: int) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_many(
            self,
            limit: int | None = None,
            offset: int | None = None,
            params: dict | None = None
    ) -> list[UserEntity]:
        ...

    @abstractmethod
    async def update_one(self, user_id: int, values: dict) -> UserEntity:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        ...
