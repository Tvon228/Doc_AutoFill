from dishka import Provider, Scope, provide

from src.backend.infrastructure.adapters.password_hasher import BcryptPasswordHasher
from src.backend.core.auth.interfaces.password_hasher import PasswordHasherProtocol


class PasswordHasherProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_password_hasher(self) -> PasswordHasherProtocol:
        return BcryptPasswordHasher()
