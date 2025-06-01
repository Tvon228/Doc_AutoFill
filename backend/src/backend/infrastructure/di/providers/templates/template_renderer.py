from dishka import Provider, Scope, provide

from src.backend.core.templates.interfaces.template_renderer import TemplateRendererProtocol
from src.backend.infrastructure.adapters.template_renderer import TemplateRenderer


class TemplateRendererProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_template_parser_factory(
            self,
    ) -> TemplateRendererProtocol:
        return TemplateRenderer()

