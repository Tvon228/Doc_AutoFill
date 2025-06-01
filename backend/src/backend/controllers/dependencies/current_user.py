from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, Request, HTTPException, status

from src.backend.core.auth.exceptions import InvalidTokenError
from src.backend.core.auth.interfaces import JwtEncoderBase
from src.backend.core.auth.services.auth_service import AuthService
from src.backend.core.auth.services.role_privilege import RolePrivilegeService
from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.core.users.entity import UserEntity
from src.backend.main.config import config


def fetch_access_token(request: Request) -> str:
    access_token: str = request.cookies.get(config.auth.access_cookie_name)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not passed")
    return access_token


@inject
async def get_current_user(
        request: Request,
        auth_service: FromDishka[AuthService],
        jwt_encoder: FromDishka[JwtEncoderBase]
) -> UserEntity:
    access_token = fetch_access_token(request=request)
    try:
        user: UserEntity = await auth_service.authenticate_user(
            access_token=access_token,
            jwt_encoder=jwt_encoder
        )
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return user


CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]


def require_role(required_role: UserRoleEnum, exact_match: bool = False):

    def dependency(current_user: CurrentUserDep):
        has_privilege: bool = RolePrivilegeService.has_privilege(
            user_role=current_user.role,
            required_role=required_role,
            exact_match=exact_match,
        )

        if not has_privilege:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges",
            )
        return current_user

    return dependency


AdminUserDep = Annotated[
    UserEntity,
    Depends(require_role(required_role=UserRoleEnum.ADMIN))
]

MainAdminDep = Annotated[
    UserEntity,
    Depends(require_role(required_role=UserRoleEnum.MAIN_ADMIN))
]
