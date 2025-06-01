from typing import Self

from src.backend.core.auth.interfaces import JwtEncoderBase, PasswordHasherProtocol
from src.backend.core.auth.utils import is_token_expired, get_tokens_pair, get_access_token
from src.backend.core.auth.dto import LoginRequestDTO, UserWithTokenDTO, TokenDTO
from src.backend.core.common.utils.phones import try_parse_phone_number
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.users.exceptions import UserNotFoundError
from src.backend.core.common.utils.is_email import is_email
from src.backend.core.users.repo import UsersRepositoryProtocol
from src.backend.core.users.entity import UserEntity
from src.backend.core.auth.exceptions import (
    LoginOrPasswordInvalidError,
    TokenExpiredError,
    JwtSubNotPassedError,
)


class AuthService:

    def __init__(self: Self, users_repo: UsersRepositoryProtocol, session: SessionProtocol):
        self.users_repo: UsersRepositoryProtocol = users_repo
        self.session: SessionProtocol = session

    async def get_users_with_login(self, login: str) -> list[UserEntity]:
        """
        Получить пользователей по логину (телефон / почта / имя)
        - Для телефона/почты: список из 0 или 1 элемента
        - Для имени: список всех совпадений
        """
        users: list[UserEntity] = []
        user: UserEntity

        if phone_number := try_parse_phone_number(login):
            user = await self.users_repo.get_by_phone(phone=phone_number)
            if user:
                users.append(user)
        elif is_email(login):
            user = await self.users_repo.get_by_email(email=login)
            if user:
                users.append(user)
        else:
            users = await self.users_repo.get_by_name(name=login)

        return users

    @staticmethod
    def match_user_by_password(
            users: list,
            password: str,
            password_hasher: PasswordHasherProtocol,
    ) -> UserEntity | None:

        for user in users:
            is_password_correct: bool = password_hasher.verify(password, user.password_hash)
            if is_password_correct:
                return user
        return None

    async def login_and_get_token(
            self,
            login_data: LoginRequestDTO,
            password_hasher: PasswordHasherProtocol,
            jwt_encoder: JwtEncoderBase
    ) -> UserWithTokenDTO:
        # Ищем пользователей по введённому логину
        users: list[UserEntity] = await self.get_users_with_login(login=login_data.login)

        # Проверяем, что хотя бы у одного пароль подходит
        password: str = login_data.password
        user = self.match_user_by_password(users=users, password=password, password_hasher=password_hasher)
        if not user:
            raise LoginOrPasswordInvalidError

        tokens_data = get_tokens_pair(user_id=user.id, jwt_encoder=jwt_encoder)
        return UserWithTokenDTO(user=user, token=tokens_data)

    async def refresh(self, refresh_token: str, jwt_encoder: JwtEncoderBase) -> str:
        payload: dict = jwt_encoder.decode(refresh_token)
        if is_token_expired(payload):
            raise TokenExpiredError
        access_token = get_access_token(user_id=payload.get("sub"), jwt_encoder=jwt_encoder)
        return access_token

    async def authenticate_user(self, access_token: str, jwt_encoder: JwtEncoderBase) -> UserEntity:
        payload: dict = jwt_encoder.decode(access_token)
        if is_token_expired(payload):
            raise TokenExpiredError
        user = await self._get_user_from_payload(payload)
        return user

    async def _get_user_from_payload(self, payload: dict) -> UserEntity:
        user_id = payload.get("sub")
        if not user_id:
            raise JwtSubNotPassedError

        user = await self.users_repo.get_by_id(int(user_id))
        if not user:
            raise UserNotFoundError
        return user
