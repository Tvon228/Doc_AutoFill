from dishka import Provider, Scope, provide

from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.templates.repositories.template_fields import TemplateFieldsRepositoryProtocol
from src.backend.core.templates.services.template_fields import TemplateFieldsService


class TemplateFieldsServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_template_fields_service(
            self,
            session: SessionProtocol,
            template_fields_repo: TemplateFieldsRepositoryProtocol,
    ) -> TemplateFieldsService:
        return TemplateFieldsService(
            session=session,
            template_fields_repo=template_fields_repo
        )
