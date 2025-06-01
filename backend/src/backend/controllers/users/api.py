from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute
from dishka import FromDishka

from src.backend.infrastructure.db.users.mappers import map_user_model_to_entity
from src.backend.core.auth.interfaces import PasswordHasherProtocol
from src.backend.controllers.users.schemas import UpdateUserSchema, SingleUserResponse, UserResponseSchema, \
    ListUsersResponse, DeleteUserResponse
from src.backend.core.users.dto import AddUserDTO, UpdateUserDTO
from src.backend.core.users.exceptions import UserNotFoundError
from src.backend.controllers.auth.schemas import AddUserSchema
from src.backend.controllers.dependencies.current_user import (
    CurrentUserDep,
    AdminUserDep,
    MainAdminDep
)

from src.backend.core.users.service import UsersService
from src.backend.core.users.entity import UserId


router: APIRouter = APIRouter(route_class=DishkaRoute, prefix="/users", tags=["Пользователи"])


@router.post("/", response_model=SingleUserResponse)
async def create_user(
        user_data: AddUserSchema,
        admin_user: AdminUserDep,
        password_hasher: FromDishka[PasswordHasherProtocol],
        user_service: FromDishka[UsersService],
):
    """Создать нового пользователя"""
    requesting_user = map_user_model_to_entity(admin_user)
    new_user_data = AddUserDTO(added_by_user_id=UserId(requesting_user.id), **user_data.model_dump())
    new_user = await user_service.create_user(requesting_user, new_user_data, password_hasher)
    return {"user": UserResponseSchema.model_validate(new_user)}


@router.get("/", response_model=ListUsersResponse)
async def get_all_users(
        users_service: FromDishka[UsersService],
        main_admin: MainAdminDep
):
    """Получить всех пользователей"""
    users = await users_service.get_all()
    return {"users": [UserResponseSchema.model_validate(user) for user in users]}


@router.get("/added-by-me", response_model=ListUsersResponse)
async def get_users_added_by_me(
        users_service: FromDishka[UsersService],
        admin_user: AdminUserDep
):
    """Пользователи, добавленные текущим пользователем"""
    users = await users_service.get_added_by_user(user_id=admin_user.id)
    return {"users": [UserResponseSchema.model_validate(user) for user in users]}


@router.get("/me", response_model=SingleUserResponse)
async def get_my_profile(
        user: CurrentUserDep,
):
    """Профиль текущего пользователя"""
    return {"user": UserResponseSchema.model_validate(user)}


@router.patch("/{user_id}", response_model=SingleUserResponse)
async def edit_user(
        user_id: int,
        update_data: UpdateUserSchema,
        current_user: CurrentUserDep,
        users_service: FromDishka[UsersService],
):
    """Изменить пользователя"""
    update_dto = UpdateUserDTO(**update_data.model_dump())
    updated_user = await users_service.update_user(
        user_id=user_id,
        requesting_user=current_user,
        update_data=update_dto
    )
    return {"user": UserResponseSchema.model_validate(updated_user)}


@router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        requesting_user: CurrentUserDep,
        users_service: FromDishka[UsersService],
):
    """Удалить пользователя"""
    try:
        is_deleted = await users_service.delete_user(requesting_user, user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"detail": "ok", "is_deleted": is_deleted}
