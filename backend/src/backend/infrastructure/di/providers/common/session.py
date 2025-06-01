from typing import AsyncGenerator

from dishka import provide, Scope, Provider

from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.infrastructure.db.engine import async_session_maker


class SessionProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_session(self) -> AsyncGenerator[SessionProtocol, None]:
        async with async_session_maker() as session:
            yield session
