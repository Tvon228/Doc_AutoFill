from dishka import Provider, Scope, provide

from src.backend.core.templates.repositories.template_fields import TemplateFieldsRepositoryProtocol
from src.backend.infrastructure.db.templates.template_fields.repo import TemplateFieldsRepository
from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.core.common.interfaces.session import SessionProtocol


class TemplateFieldsRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_template_fields_repo(
            self,
            session: SessionProtocol
    ) -> TemplateFieldsRepositoryProtocol:
        crud_repo: SqlAlchemyCrudRepo = SqlAlchemyCrudRepo(
            model=TemplateFieldsRepository.model,
            session=session
        )
        return TemplateFieldsRepository(session=session, crud_repo=crud_repo)
