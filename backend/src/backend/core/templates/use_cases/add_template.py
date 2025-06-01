from typing import BinaryIO

from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol
from src.backend.core.templates.entities import TemplateEntity, TemplateId
from src.backend.core.templates.interfaces.template_editor import TemplateParserFactoryProtocol
from src.backend.core.templates.services.template_fields import TemplateFieldsService
from src.backend.core.templates.services.templates import TemplatesService


class UploadTemplateFileUseCase:

    def __init__(
            self,
            templates_service: TemplatesService,
            template_fields_service: TemplateFieldsService,
            files_storage: FilesStorageProtocol,
            template_parser_factory: TemplateParserFactoryProtocol
    ):
        self.templates_service: TemplatesService = templates_service
        self.vars_service: TemplateFieldsService = template_fields_service

        self.files_storage: FilesStorageProtocol = files_storage
        self.template_parser_factory: TemplateParserFactoryProtocol = template_parser_factory

    async def execute(
            self,
            template_id: int,
            file_name: str,
            file_content: BinaryIO
    ) -> None:
        await self.templates_service.upload(
            template_id=template_id,
            file_content=file_content,
            files_storage=self.files_storage,
            file_name=file_name
        )
        template: TemplateEntity = await self.templates_service.get(ident=TemplateId(template_id))
        template_parser = self.template_parser_factory.create(file_io=file_content)
        await self.vars_service.save_from_template(
            template=template, template_parser=template_parser
        )
  