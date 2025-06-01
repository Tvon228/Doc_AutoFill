from dishka import Provider, Scope, provide

from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.templates.repositories.templates import TemplatesRepositoryProtocol
from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.infrastructure.db.templates.templates.repo import TemplatesRepository


class TemplatesRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_templates_repo(
            self,
            session: SessionProtocol
    ) -> TemplatesRepositoryProtocol:
        crud_repo: SqlAlchemyCrudRepo = SqlAlchemyCrudRepo(
            session=session,
            model=TemplatesRepository.model,
        )
        return TemplatesRepository(crud_repo=crud_repo, session=session)
