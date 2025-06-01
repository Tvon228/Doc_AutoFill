import xml.etree.ElementTree as ET
from zipfile import ZipFile
from io import BytesIO
import re

from jinja2schema.model import List, Scalar
import jinja2schema

from src.backend.core.templates.interfaces.template_editor import TemplateParserProtocol
from src.backend.core.templates.enums import FieldTypeEnum


class DocxFieldsParser:
    """
    Получает xml из docx файла и ищет через регулярные выражения все поля вида {{...}} или {% ... %}
    """

    def __init__(self, docx_file_io: BytesIO):
        self.file = docx_file_io
        self.__xml_namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    def fetch_all_fields(self) -> list[str]:
        xml_str = self.xml_string_from_docx()
        root = ET.fromstring(xml_str)

        all_fields = []
        for xml_paragraph in root.findall('.//w:p', namespaces=self.__xml_namespaces):
            paragraph_text: str | None = self.get_paragraph_text(xml_paragraph)
            if not paragraph_text:
                continue

            paragraph_fields = self._fetch_fields(paragraph_text)
            all_fields.extend(paragraph_fields)
        return all_fields

    def xml_string_from_docx(self) -> str:
        with ZipFile(self.file) as docx_zip:
            xml = docx_zip.read("word/document.xml").decode("utf-8")
            return xml

    @staticmethod
    def _get_variable_fields(string: str) -> list[str]:
        return re.findall(pattern=r"{{\s*.*?\s*}}", string=string)

    @classmethod
    def _fetch_fields(cls, string: str) -> list[str]:
        variable_fields = cls._get_variable_fields(string)
        expressions_fields = re.findall(pattern=r"{%\s*[\s\w]+\s*%}", string=string)
        return variable_fields + expressions_fields

    @classmethod
    def fetch_variables(cls, string: str) -> set[str]:
        fields = cls._get_variable_fields(string)
        result = set()
        for field in fields:
            variables = re.findall(pattern=r"\b\w+(?:\.\w+)?\b", string=field)
            result.update(variables)
        return result

    def get_paragraph_text(self, paragraph: ET.Element) -> str | None:
        texts = [
            node.text
            for node in paragraph.findall('.//w:t', namespaces=self.__xml_namespaces)
            if node.text
        ]
        if not texts:
            return None
        return ''.join(texts)


class DocxSchemaParser(TemplateParserProtocol):

    def __init__(
            self,
            docx_file_io: BytesIO,
            ignore_tags: list[str] = None
    ):
        self.file = docx_file_io
        self.ignore_tags = ignore_tags

    def extract_flat_schema(self) -> dict[str, FieldTypeEnum]:
        raw_fields = self._load_template_fields()
        schema_dict = jinja2schema.infer("".join(raw_fields))
        return self._flatten_schema(schema_dict)

    def extract_nested_schema(self) -> dict[str, FieldTypeEnum | dict]:
        raw_fields = self._load_template_fields()
        schema_dict = jinja2schema.infer("".join(raw_fields))
        return self._nested_schema(schema_dict)

    def _remove_ignore_tags(self, raw_fields: list[str]) -> list[str]:
        """
        Удаляет теги (например, tr из выражений вида {%tr for ... %}).
        """
        cleaned_fields = []
        for field in raw_fields:
            for tag in self.ignore_tags:
                pattern = r"({%\s*)" + re.escape(tag) + r"(\b)"
                field = re.sub(pattern=pattern, repl=r"\1\2", string=field)
            cleaned_fields.append(field)
        return cleaned_fields

    @staticmethod
    def _flatten_schema(jinja_schema: dict) -> dict[str, FieldTypeEnum]:
        """
        Преобразует схему в плоский словарь
        """
        flat_schema = {}

        for key, value in jinja_schema.items():
            if isinstance(value, List):
                # Пример: Специалисты -> спец.ФИО
                for sub_key in value.item.keys():
                    flat_schema[f"{value.label}.{sub_key}"] = FieldTypeEnum.OBJ_ATTR
            elif isinstance(value, Scalar):
                flat_schema[key] = FieldTypeEnum.SCALAR

        return flat_schema

    @staticmethod
    def _nested_schema(jinja_schema: dict) -> dict[str, FieldTypeEnum | dict]:
        """
        Преобразует схему в виде словаря с вложенностью
        """
        nested = {}
        for key, value in jinja_schema.items():
            if isinstance(value, List):
                nested[key] = {
                    sub_key: FieldTypeEnum.OBJ_ATTR
                    for sub_key in value.item.keys()
                }
            elif isinstance(value, Scalar):
                nested[key] = FieldTypeEnum.SCALAR
        return nested

    def _load_template_fields(self) -> list[str]:
        """
        Извлекает все шаблонные поля из .docx как список строк.
        """
        parser = DocxFieldsParser(docx_file_io=self.file)
        fields = parser.fetch_all_fields()
        if self.ignore_tags:
            fields = self._remove_ignore_tags(fields)
        return fields