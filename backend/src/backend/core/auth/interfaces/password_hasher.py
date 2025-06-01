from typing import Protocol


class PasswordHasherProtocol(Protocol):

    def hash(self, password: str) -> str:
        """ Получить хеш пароля """
        raise NotImplementedError

    def verify(self, password: str, hashed_password: str) -> bool:
        """ Проверить, что пароли совпадают """
        raise NotImplementedError
