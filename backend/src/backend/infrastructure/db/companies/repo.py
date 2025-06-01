from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.core.companies.repo import CompaniesRepositoryProtocol
from src.backend.core.auth.exceptions import LoginAlreadyInUseError
from src.backend.core.common.exceptions import AlreadyExistsError
from src.backend.infrastructure.db.companies.mappers import (
    map_company_models_to_entities,
    map_company_model_to_entity
)
from src.backend.core.companies.entity import CompanyEntity
from src.backend.core.companies.dto import AddCompanyDTO
from src.backend.infrastructure.db import CompanyModel
from src.backend.core.users.entity import UserEntity


class CompaniesRepository(CompaniesRepositoryProtocol):

    model = CompanyModel

    def __init__(self, session: AsyncSession, crud_repo: SqlAlchemyCrudRepo):
        self.session = session
        self.crud_repo: SqlAlchemyCrudRepo = crud_repo

    async def create(self, data: AddCompanyDTO) -> CompanyEntity | None:
        try:
            company_model: CompanyModel = await self.crud_repo.create(
                title=data.title,
                created_by_id=data.created_by_id,
            )
        except AlreadyExistsError:
            raise LoginAlreadyInUseError
        return map_company_model_to_entity(company_model)

    async def get_by_user(self, user: UserEntity) -> list[CompanyEntity]:
        ids = [user.id]
        if user.added_by_user_id is not None:
            ids.append(user.added_by_user_id)
        query =  select(self.model).where(self.model.created_by_id.in_(ids))

        result = await self.session.execute(query)
        values = result.scalars().all()
        return map_company_models_to_entities(values)

    async def get_many(
            self, limit: int | None = None,
            offset: int | None = None,
            params: dict | None = None
    ) -> list[CompanyEntity]:
        if not params:
            params = {}

        result = await self.crud_repo.get_all(
            limit=limit,
            offset=offset,
            **params
        )
        return map_company_models_to_entities(models=result)

    async def __get_by_params(self, **kwargs) -> UserEntity | None:
        company: CompanyModel = await self.crud_repo.get_one(**kwargs)
        return map_company_model_to_entity(company) if company else None

    async def get_by_id(self, ident: int) -> CompanyEntity | None:
        return await self.__get_by_params(id=ident)

    async def delete(self, company_id: int) -> bool:
        user: CompanyModel | None = await self.session.get(ident=company_id, entity=self.model)
        if user:
            await self.session.delete(user)
            return True
        return False

