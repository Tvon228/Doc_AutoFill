from dishka import Provider, Scope, provide, from_context

from src.backend.infrastructure.adapters.jwt_encoder import JwtEncoder
from src.backend.core.auth.interfaces import JwtEncoderBase
from src.backend.main.config import AuthConfig


class JwtEncoderProvider(Provider):
    scope = Scope.REQUEST

    auth_config: AuthConfig = from_context(provides=AuthConfig, scope=Scope.APP)

    @provide
    def provide_jwt_encoder(
            self,
            auth_config: AuthConfig,
    ) -> JwtEncoderBase:
        return JwtEncoder(
            secret_key=auth_config.secret_key,
            algorithm=auth_config.algorithm
        )
