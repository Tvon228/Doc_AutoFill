from abc import abstractmethod
from typing import Protocol

from src.backend.core.companies.entity import CompanyEntity
from src.backend.core.companies.dto import AddCompanyDTO
from src.backend.core.users.entity import UserEntity


class CompaniesRepositoryProtocol(Protocol):

    @abstractmethod
    async def create(self, data: AddCompanyDTO) -> CompanyEntity | None:
        ...

    @abstractmethod
    async def get_by_id(self, ident: int) -> CompanyEntity | None:
        ...

    @abstractmethod
    async def get_by_user(self, user: UserEntity) -> list[CompanyEntity]:
        ...

    @abstractmethod
    async def get_many(
            self,
            limit: int | None = None,
            offset: int | None = None,
            params: dict | None = None
    ) -> list[CompanyEntity]:
        ...

    @abstractmethod
    async def delete(self, company_id: int) -> bool:
        ...
