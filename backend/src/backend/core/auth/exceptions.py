from src.backend.core.common.exceptions import AppError


class LoginAlreadyInUseError(AppError):
    @property
    def message(self) -> str | None:
        return None


class LoginOrPasswordInvalidError(AppError):
    @property
    def message(self) -> str | None:
        return "Login or password invalid!"


class PermissionDeniedError(AppError):
    @property
    def message(self) -> str | None:
        return "Not enough permissions!"


# JWT Token
class InvalidTokenError(AppError):
    @property
    def message(self) -> str | None:
        return "Token is invalid!"


class JwtDecodeError(InvalidTokenError):
    @property
    def message(self) -> str | None:
        return "Failed to decode token!"


class TokenExpiredError(InvalidTokenError):
    @property
    def message(self) -> str | None:
        return "Token expired!"


class JwtExpiresNotPassedError(InvalidTokenError):
    @property
    def message(self) -> str | None:
        return "Expires field not passed!"


class JwtSubNotPassedError(InvalidTokenError):
    @property
    def message(self) -> str | None:
        return "Sub field not passed!"
