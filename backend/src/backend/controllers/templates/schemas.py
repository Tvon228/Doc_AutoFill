from typing import Any

from pydantic import BaseModel

from src.backend.core.templates.enums import FieldTypeEnum, FieldDataTypeEnum


class AddTemplateSchema(BaseModel):
    company_id: int


class TemplateSchema(BaseModel):
    id: int
    company_id: int

    class Config:
        from_attributes = True


class ResponseTemplateSchema(BaseModel):
    detail: str = "ok"
    template: TemplateSchema


class ResponseTemplatesSchema(BaseModel):
    detail: str = "ok"
    templates: list[TemplateSchema]



class TemplateFieldSchema(BaseModel):
    name: str
    template_id: int
    field_type: FieldTypeEnum
    data_type: FieldDataTypeEnum = FieldDataTypeEnum.TEXT

    class Config:
        from_attributes = True


class ResponseTemplateFieldsSchema(BaseModel):
    detail: str = "ok"
    fields: list[TemplateFieldSchema]


class RenderTemplateSchema(BaseModel):
    data: dict[str, Any]