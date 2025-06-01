from typing import Iterable

from src.backend.infrastructure.db.templates.template_fields.model import TemplateFieldModel
from src.backend.core.templates.entities import TemplateFieldEntity, TemplateId


def map_template_field_model_to_entity(model: TemplateFieldModel) -> TemplateFieldEntity:
    return TemplateFieldEntity(
        name=model.name,
        template_id=TemplateId(model.template_id),
        data_type=model.data_type,
        type=model.field_type,
    )


def map_template_field_models_to_entities(models: Iterable[TemplateFieldModel]) -> list[TemplateFieldEntity]:
    return [
        map_template_field_model_to_entity(model=model)
        for model in models
    ]
