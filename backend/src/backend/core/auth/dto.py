from dataclasses import dataclass

from src.backend.core.users.entity import UserEntity


@dataclass(frozen=True, slots=True)
class LoginRequestDTO:
    login: str
    password: str


@dataclass(frozen=True, slots=True)
class TokenDTO:
    access_token: str
    refresh_token: str | None = None


@dataclass(frozen=True, slots=True)
class UserWithTokenDTO:
    user: UserEntity
    token: TokenDTO
