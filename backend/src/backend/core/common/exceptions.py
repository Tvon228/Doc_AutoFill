from abc import ABC, abstractmethod


class AppError(Exception, ABC):
    """Базовое исключение для приложения"""

    @property
    @abstractmethod
    def message(self) -> str | None:
        return None

    def __init__(self, detail: str | None = None):
        msg = detail if detail is not None else self.message
        super().__init__(msg if msg is not None else "")

    def __repr__(self) -> str:
        class_name: str = type(self).__name__
        if self.message is not None:
            return f"{class_name}: {self.message}"
        return class_name


class NotFoundError(AppError):
    @property
    def message(self) -> str | None:
        return "Instance not found"


class AlreadyExistsError(AppError):
    @property
    def message(self) -> str | None:
        return "Instance already exists"
