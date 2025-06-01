from abc import abstractmethod
from typing import Protocol
from io import BytesIO

from src.backend.core.templates.enums import FieldTypeEnum


class TemplateParserProtocol(Protocol):

    def extract_flat_schema(self) -> dict[str, FieldTypeEnum]:
        """
        Возвращает схему шаблона в плоском виде:
        {'ФИО': SCALAR, 'Специалисты.ФИО': OBJ_ATTR, ...}
        """
        ...

    def extract_nested_schema(self) -> dict[str, FieldTypeEnum | dict]:
        """
        Возвращает схему с вложенностью:
        """
        ...


class TemplateParserFactoryProtocol:
    @abstractmethod
    def create(self, file_io: BytesIO) -> TemplateParserProtocol:
        ...
