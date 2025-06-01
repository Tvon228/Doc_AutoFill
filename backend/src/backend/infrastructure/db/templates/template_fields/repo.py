from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.backend.core.templates.repositories.template_fields import TemplateFieldsRepositoryProtocol
from src.backend.infrastructure.db.templates.template_fields.model import TemplateFieldModel
from src.backend.core.templates.entities import TemplateFieldEntity, TemplateId
from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.infrastructure.db.templates.template_fields.mappers import (
    map_template_field_model_to_entity,
    map_template_field_models_to_entities
)
from src.backend.core.templates.dtos import AddTemplateFieldDTO


class TemplateFieldsRepository(TemplateFieldsRepositoryProtocol):
    model = TemplateFieldModel

    def __init__(self, session: AsyncSession, crud_repo: SqlAlchemyCrudRepo):
        self.session: AsyncSession = session
        self.crud_repo: SqlAlchemyCrudRepo = crud_repo

    async def save(self, data: AddTemplateFieldDTO) -> TemplateFieldEntity:
        result = await self.crud_repo.create()
        return map_template_field_model_to_entity(model=result)

    async def save_many(self, fields_data: Iterable[AddTemplateFieldDTO]) -> list[TemplateFieldEntity]:
        fields: list[TemplateFieldEntity] = []

        for data in fields_data:
            field = await self.crud_repo.create(
                name=data.name,
                template_id=data.template_id,
                field_type=data.field_type,
                data_type=data.data_type
            )
            fields.append(field)

        return fields

    async def get_unique(self, template_ids: list[TemplateId]) -> list[TemplateFieldEntity]:
        query = (
            select(self.model)
            .distinct(self.model.name)
            .where(self.model.template_id.in_(template_ids))
            .order_by(self.model.name)
        )
        result = (await self.session.execute(query)).scalars().all()
        return map_template_field_models_to_entities(result)