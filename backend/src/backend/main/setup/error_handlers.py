from typing import Callable, Awaitable

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.backend.core.auth.exceptions import PermissionDeniedError, JwtDecodeError


def create_exception_handler(status_code: int) -> Callable[[Request, Exception], Awaitable[Response]]:
    async def handler(request: Request, exc: Exception) -> Response:
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)}
        )
    return handler


def add_error_handlers(app: FastAPI):
    app.add_exception_handler(
        JwtDecodeError,
        create_exception_handler(status.HTTP_401_UNAUTHORIZED)
    )

    app.add_exception_handler(
        PermissionDeniedError,
        create_exception_handler(status.HTTP_403_FORBIDDEN)
    )

