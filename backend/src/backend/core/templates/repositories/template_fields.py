from typing import Protocol, Iterable

from src.backend.core.templates.entities import TemplateFieldEntity
from src.backend.core.templates.dtos import AddTemplateFieldDTO


class TemplateFieldsRepositoryProtocol(Protocol):

    async def save(self, data: AddTemplateFieldDTO) -> TemplateFieldEntity:
        ...

    async def save_many(self, fields_data: Iterable[AddTemplateFieldDTO]) -> list[TemplateFieldEntity]:
        ...

    async def get_unique(self, template_ids: list[int]) -> list[TemplateFieldEntity]:
        ...
