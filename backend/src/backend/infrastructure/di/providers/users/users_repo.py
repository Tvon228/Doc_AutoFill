from dishka import Provider, Scope, provide

from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.infrastructure.db.users.repo import UsersRepository
from src.backend.core.users.repo import UsersRepositoryProtocol


class UsersRepoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_users_repo(
            self,
            session: SessionProtocol,
    ) -> UsersRepositoryProtocol:
        crud_repo: SqlAlchemyCrudRepo = SqlAlchemyCrudRepo(model=UsersRepository.model, session=session)
        return UsersRepository(session=session, crud_repo=crud_repo)
