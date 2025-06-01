from typing import Protocol

from src.backend.core.templates.entities import TemplateEntity, TemplateId
from src.backend.core.templates.dtos import AddTemplateDTO


class TemplatesRepositoryProtocol(Protocol):

    async def add(self, data: AddTemplateDTO) -> TemplateEntity:
        ...

    async def get(self, ident: TemplateId) -> TemplateEntity | None:
        ...

    async def get_by_company(self, company_id: int) -> list[TemplateEntity]:
        ...

    async def get_by_ids(self, template_ids: list[TemplateId]) -> list[TemplateEntity]:
        ...

    async def set_file_name(self, template_id: int, file_name: str) -> TemplateEntity:
        ...
