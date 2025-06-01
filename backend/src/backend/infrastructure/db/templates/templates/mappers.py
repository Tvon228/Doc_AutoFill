from typing import Iterable

from src.backend.core.companies.entity import CompanyId
from src.backend.core.templates.entities import TemplateEntity
from src.backend.infrastructure.db.templates.templates.model import TemplateModel


def map_template_model_to_entity(model: TemplateModel) -> TemplateEntity:
    return TemplateEntity(
        id=model.id,
        file_name=model.file_name,
        company_id=CompanyId(model.company_id),
    )


def map_template_models_to_entities(models: Iterable[TemplateModel]) -> list[TemplateEntity]:
    return [map_template_model_to_entity(model) for model in models]
