from dishka import Provider, Scope, provide

from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.users.repo import UsersRepositoryProtocol
from src.backend.core.users.service import UsersService


class UsersServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_users_service(
            self,
            users_repo: UsersRepositoryProtocol,
            session: SessionProtocol,
    ) -> UsersService:
        return UsersService(session=session, users_repo=users_repo)
