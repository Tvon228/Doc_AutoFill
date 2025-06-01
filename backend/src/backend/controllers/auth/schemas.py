from pydantic import BaseModel, EmailStr

from src.backend.core.common.enums.user_roles import UserRoleEnum


class AddUserSchema(BaseModel):
    name: str
    password: str
    role: UserRoleEnum = UserRoleEnum.EMPLOYEE


class RecoverPasswordSchema(BaseModel):
    email: EmailStr
