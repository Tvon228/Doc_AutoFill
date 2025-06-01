from dishka import Provider, Scope, provide

from src.backend.core.auth.services.auth_service import AuthService
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.users.repo import UsersRepositoryProtocol


class AuthServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_auth_service(
            self,
            users_repo: UsersRepositoryProtocol,
            session: SessionProtocol
    ) -> AuthService:
        return AuthService(users_repo=users_repo, session=session)
