from fastapi import FastAPI

from src.backend.controllers.templates.api import router as templates_router
from src.backend.controllers.companies.api import router as companies_router
from src.backend.controllers.users.api import router as users_router
from src.backend.controllers.auth.api import router as auth_router


def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(companies_router)
    app.include_router(templates_router)
