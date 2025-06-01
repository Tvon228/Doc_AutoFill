from dishka.integrations.fastapi import setup_dishka
from dishka import AsyncContainer
from fastapi import FastAPI

from src.backend.core.auth.interfaces import PasswordHasherProtocol
from src.backend.core.users.service import UsersService
from src.backend.main.setup.error_handlers import add_error_handlers
from src.backend.main.setup.include_routers import include_routers
from src.backend.infrastructure.di.container import get_async_container
from src.backend.main.config import config


async def create_main_admin(
        users_service: UsersService,
        password_hasher: PasswordHasherProtocol
) -> None:
    await users_service.create_main_admin_if_not_exists(
        email=config.app.main_admin_email,
        password=config.app.main_admin_password,
        password_hasher=password_hasher
    )
    await users_service.session.commit()


def get_startup_event_handler(container: AsyncContainer):
    async def startup_event_handler():
        async with container() as nested_container:
            users_service = await nested_container.get(UsersService)
            password_hasher = await nested_container.get(PasswordHasherProtocol)
            await create_main_admin(users_service=users_service, password_hasher=password_hasher)

    return startup_event_handler


def setup(app: FastAPI) -> None:
    include_routers(app)
    add_error_handlers(app)

    container = get_async_container(config)
    setup_dishka(container, app)

    app.add_event_handler("startup", get_startup_event_handler(container))
