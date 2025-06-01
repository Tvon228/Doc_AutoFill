from dishka import Provider, Scope, provide

from src.backend.core.templates.interfaces.template_editor import TemplateParserFactoryProtocol
from src.backend.core.templates.use_cases.add_template import UploadTemplateFileUseCase
from src.backend.core.templates.services.template_fields import TemplateFieldsService
from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol
from src.backend.core.templates.services.templates import TemplatesService


class AddTemplateUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_add_template_use_case(
            self,
            templates_service: TemplatesService,
            template_fields_service: TemplateFieldsService,
            files_storage: FilesStorageProtocol,
            template_parser_factory: TemplateParserFactoryProtocol
    ) -> UploadTemplateFileUseCase:
        return UploadTemplateFileUseCase(
            templates_service=templates_service,
            template_fields_service=template_fields_service,
            files_storage=files_storage,
            template_parser_factory=template_parser_factory
        )
