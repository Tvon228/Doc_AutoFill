from dishka import Provider, Scope, provide

from src.backend.core.templates.repositories.templates import TemplatesRepositoryProtocol
from src.backend.core.templates.services.templates import TemplatesService
from src.backend.core.common.interfaces.session import SessionProtocol


class TemplatesServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_templates_service(
            self,
            session: SessionProtocol,
            templates_repo: TemplatesRepositoryProtocol,
    ) -> TemplatesService:
        return TemplatesService(
            templates_repo=templates_repo,
            session=session
        )
