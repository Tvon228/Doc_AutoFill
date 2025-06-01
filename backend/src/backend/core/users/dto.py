from dataclasses import dataclass

from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.core.users.entity import UserId


@dataclass(frozen=True, slots=True)
class AddUserDTO:
    name: str
    password: str
    role: UserRoleEnum
    added_by_user_id: UserId | None = None
    email: str | None = None
    phone: int | None = None


@dataclass(slots=True)
class UpdateUserDTO:
    name: str | None = None
    email: str | None = None
    phone: int | None = None
