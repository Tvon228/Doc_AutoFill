from abc import ABC, abstractmethod
from datetime import timedelta


class JwtEncoderBase(ABC):

    def __init__(self, secret_key: str, algorithm: str):
        self._key = secret_key
        self._algorithm = algorithm

    @abstractmethod
    def create_token(self, data: dict, expires: timedelta) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> dict:
        """
        Returns:
            dict - payload токена
        Raises:
            JwtDecodeError: При ошибке валидации
        """
        raise NotImplementedError
