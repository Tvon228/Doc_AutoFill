from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from src.backend.core.common.enums.user_roles import UserRoleEnum


class UpdateUserSchema(BaseModel):
    name: str | None = Field(None, min_length=1)
    phone: int | None = None
    email: EmailStr | None = None


class UserResponseSchema(BaseModel):
    id: int
    name: str
    registered_at: datetime
    role: UserRoleEnum = UserRoleEnum.EMPLOYEE
    added_by_user_id: int | None = None
    email: str | None = None
    phone: int | None = None

    class Config:
        from_attributes = True


class DeleteUserResponse(BaseModel):
    detail: str
    is_deleted: bool


class SingleUserResponse(BaseModel):
    detail: str = "ok"
    user: UserResponseSchema


class ListUsersResponse(BaseModel):
    detail: str = "ok"
    users: list[UserResponseSchema]

