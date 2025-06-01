from src.backend.core.common.exceptions import NotFoundError


class UserNotFoundError(NotFoundError):
    @property
    def message(self) -> str | None:
        return "User not found!"
