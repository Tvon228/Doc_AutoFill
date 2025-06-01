from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from src.backend.core.common.enums.user_roles import UserRoleEnum


UserId = NewType("UserId", int)


@dataclass(slots=True, frozen=True)
class UserEntity:
    id: UserId
    name: str
    password_hash: str
    role: UserRoleEnum
    registered_at: datetime
    added_by_user_id: UserId | None = None
    email: str | None = None
    phone: int | None = None
    photo: str | None = None
