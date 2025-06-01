from collections import defaultdict

from src.backend.core.templates.repositories.template_fields import TemplateFieldsRepositoryProtocol
from src.backend.core.templates.interfaces.template_editor import TemplateParserProtocol
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.templates.dtos import AddTemplateFieldDTO
from src.backend.core.templates.entities import TemplateEntity
from src.backend.core.templates.enums import FieldTypeEnum


class TemplateFieldsService:

    def __init__(
            self,
            session: SessionProtocol,
            template_fields_repo: TemplateFieldsRepositoryProtocol,
    ):
        self.session: SessionProtocol = session
        self.fields_repo: TemplateFieldsRepositoryProtocol = template_fields_repo

    async def save_from_template(
            self,
            template: TemplateEntity,
            template_parser: TemplateParserProtocol,
    ) -> None:
        variables: dict[str, FieldTypeEnum] = template_parser.extract_flat_schema()
        add_fields_data = (
            AddTemplateFieldDTO(template_id=template.id, name=var_name, field_type=var_type)
            for var_name, var_type in variables.items()
        )
        await self.fields_repo.save_many(fields_data=add_fields_data)
        await self.session.commit()

    async def get_unique(self, template_ids: list[int]) -> dict:
        fields = await self.fields_repo.get_unique(template_ids=template_ids)
        result: defaultdict[str, FieldTypeEnum | dict] = defaultdict(dict)
        for field in fields:
            if "." in field.name:
                table_name, var_name = field.name.split(".")
                result[table_name][var_name] = FieldTypeEnum.OBJ_ATTR
            else:
                result[field.name] = FieldTypeEnum.SCALAR
        return dict(result)

