from src.backend.core.common.exceptions import AppError


class InvalidFileError(AppError):

    @property
    def message(self) -> str | None:
        return "File has invalid format!"
