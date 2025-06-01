from typing import Collection

from src.backend.core.companies.entity import CompanyEntity, CompanyId
from src.backend.infrastructure.db import CompanyModel
from src.backend.core.users.entity import UserId


def map_company_model_to_entity(model: CompanyModel) -> CompanyEntity:
    return CompanyEntity(
        id=CompanyId(model.id),
        title=model.title,
        created_by_id=UserId(model.created_by_id)
    )


def map_company_models_to_entities(models: Collection[CompanyModel]) -> list[CompanyEntity]:
    return [
        map_company_model_to_entity(model=model)
        for model in models
    ]
