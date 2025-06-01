from io import BytesIO

from dishka import Provider, Scope, provide

from src.backend.core.templates.interfaces.template_editor import TemplateParserFactoryProtocol, TemplateParserProtocol
from src.backend.infrastructure.adapters.template_parser import DocxSchemaParser


class TemplateParserFactory(TemplateParserFactoryProtocol):

    def create(self, file_io: BytesIO) -> TemplateParserProtocol:
        return DocxSchemaParser(docx_file_io=file_io, ignore_tags=["tr"])


class TemplateParserFactoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_template_parser_factory(
            self,
    ) -> TemplateParserFactoryProtocol:
        return TemplateParserFactory()

