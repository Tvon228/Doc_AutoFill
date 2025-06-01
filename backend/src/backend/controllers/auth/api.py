from fastapi import status, APIRouter, Response, HTTPException, Request
from dishka.integrations.fastapi import DishkaRoute
from dishka import FromDishka

from src.backend.controllers.schemas import DetailResponse
from src.backend.controllers.users.schemas import SingleUserResponse, UserResponseSchema
from src.backend.core.auth.interfaces import PasswordHasherProtocol, JwtEncoderBase
from src.backend.core.auth.exceptions import LoginOrPasswordInvalidError
from src.backend.core.auth.services.auth_service import AuthService
from src.backend.core.auth.dto import LoginRequestDTO
from src.backend.main.config import config


router: APIRouter = APIRouter(route_class=DishkaRoute, prefix="/auth", tags=["Авторизация",])


@router.post("/login")
async def make_login(
        response: Response,
        login_data: LoginRequestDTO,
        auth_service: FromDishka[AuthService],
        password_hasher: FromDishka[PasswordHasherProtocol],
        jwt_encoder: FromDishka[JwtEncoderBase],
) -> SingleUserResponse:
    """ Войти в аккаунт """
    try:
        data = await auth_service.login_and_get_token(
            login_data=login_data,
            password_hasher=password_hasher,
            jwt_encoder=jwt_encoder
        )
    except LoginOrPasswordInvalidError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

    response.set_cookie(
        key=config.auth.access_cookie_name,
        value=data.token.access_token,
        httponly=True
    )
    response.set_cookie(
        key=config.auth.refresh_cookie_name,
        value=data.token.refresh_token,
        httponly=True
    )

    return SingleUserResponse(detail="ok", user=UserResponseSchema.model_validate(data.user))


# @router.post("/send-recover-password")
# async def send_recover_password(
#         recover_data: RecoverPasswordSchema,
#         users_repo: UsersRepoDep,
#         auth_service: AuthServiceDep,
# ):
#     user = await users_repo.get_by_email(email=recover_data.email)
#     if not user:
#         return status.HTTP_404_NOT_FOUND


@router.post("/refresh")
async def refresh_token(
        auth_service: FromDishka[AuthService],
        jwt_encoder: FromDishka[JwtEncoderBase],
        request: Request,
        response: Response
) -> DetailResponse:
    """ Обновить access token """
    refresh_cookie: str = request.cookies.get(config.auth.refresh_cookie_name)
    if refresh_cookie is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not passed!")
    access_token: str = await auth_service.refresh(refresh_token=refresh_cookie, jwt_encoder=jwt_encoder)
    response.set_cookie(
        key=config.auth.access_cookie_name,
        value=access_token,
        httponly=True
    )
    return DetailResponse(detail="ok")


@router.post("/logout")
async def logout(response: Response) -> DetailResponse:
    """ Выйти из учётной записи """
    response.delete_cookie(config.auth.access_cookie_name)
    response.delete_cookie(config.auth.refresh_cookie_name)
    return DetailResponse(detail="Logged out")
