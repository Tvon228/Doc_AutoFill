from dataclasses import dataclass

from src.backend.core.templates.enums import FieldDataTypeEnum, FieldTypeEnum
from src.backend.core.companies.entity import CompanyId


@dataclass(frozen=True, slots=True)
class AddTemplateDTO:
    company_id: CompanyId
    file_name: str | None = None


@dataclass(frozen=True, slots=True)
class AddTemplateFieldDTO:
    template_id: int
    name: str
    field_type: FieldTypeEnum
    data_type: FieldDataTypeEnum = FieldDataTypeEnum.TEXT
