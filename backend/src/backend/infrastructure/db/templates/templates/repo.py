from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.templates.repositories.templates import TemplatesRepositoryProtocol
from src.backend.infrastructure.db.templates.templates.model import TemplateModel
from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.core.templates.entities import TemplateEntity, TemplateId
from src.backend.infrastructure.db.templates.templates.mappers import (
    map_template_model_to_entity,
    map_template_models_to_entities,
)
from src.backend.core.common.exceptions import NotFoundError
from src.backend.core.templates.dtos import AddTemplateDTO


class TemplatesRepository(TemplatesRepositoryProtocol):

    model = TemplateModel

    def __init__(self, session: AsyncSession, crud_repo: SqlAlchemyCrudRepo):
        self.session = session
        self.crud_repo: SqlAlchemyCrudRepo = crud_repo

    async def add(self, data: AddTemplateDTO) -> TemplateEntity:
        result = await self.crud_repo.create(company_id=data.company_id)
        return map_template_model_to_entity(result)

    async def get(self, ident: TemplateId) -> TemplateEntity | None:
        result = await self.crud_repo.get_by_id(ident=ident)
        return map_template_model_to_entity(result)

    async def get_by_company(self, company_id: int) -> list[TemplateEntity]:
        result = await self.crud_repo.get_all(company_id=company_id)
        return map_template_models_to_entities(result)

    async def get_by_ids(self, template_ids: list[TemplateId]) -> list[TemplateEntity]:
        query = (select(self.model).where(self.model.id.in_(template_ids)))
        result = (await self.session.execute(query)).scalars().all()
        return map_template_models_to_entities(result)

    async def set_file_name(self, template_id: int, file_name: str) -> TemplateEntity:
        template: TemplateModel | None = await self.crud_repo.get_one(id=TemplateId(template_id))
        if not template:
            raise NotFoundError
        self.session.add(template)
        await self.session.flush()
        await self.session.refresh(template)
        return map_template_model_to_entity(template)