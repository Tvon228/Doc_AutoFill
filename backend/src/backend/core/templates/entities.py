from dataclasses import dataclass
from typing import NewType

from src.backend.core.templates.enums import FieldDataTypeEnum, FieldTypeEnum
from src.backend.core.companies.entity import CompanyId


TemplateId = NewType("TemplateId", int)

@dataclass(slots=True, frozen=True)
class TemplateEntity:
    id: TemplateId
    company_id: CompanyId
    file_name: str | None = None


@dataclass(slots=True, frozen=True)
class TemplateFieldEntity:
    name: str
    template_id: TemplateId
    type: FieldTypeEnum
    data_type: FieldDataTypeEnum = FieldDataTypeEnum.TEXT


TemplateRenderId = NewType("TemplateRenderId", int)

@dataclass(slots=True, frozen=True)
class TemplateRender:
    id: TemplateId
    title: str

