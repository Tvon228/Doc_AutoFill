from dishka import Provider, Scope, provide

from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.infrastructure.db.companies.repo import CompaniesRepository
from src.backend.core.companies.repo import CompaniesRepositoryProtocol
from src.backend.core.common.interfaces.session import SessionProtocol


class CompaniesRepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_users_repo(
            self,
            session: SessionProtocol,
    ) -> CompaniesRepositoryProtocol:
        crud_repo: SqlAlchemyCrudRepo = SqlAlchemyCrudRepo(model=CompaniesRepository.model, session=session)
        return CompaniesRepository(session=session, crud_repo=crud_repo)
