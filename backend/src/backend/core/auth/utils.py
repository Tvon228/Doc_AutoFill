from datetime import datetime, timedelta, timezone

from src.backend.core.auth.dto import TokenDTO
from src.backend.core.auth.exceptions import JwtExpiresNotPassedError
from src.backend.core.auth.interfaces import JwtEncoderBase
from src.backend.core.auth.enums import TokenTypeEnum
from src.backend.main.config import config


def create_token(
        jwt_encoder: JwtEncoderBase,
        user_id: int,
        token_type: TokenTypeEnum,
        expires_minutes: int
) -> str:
    data: dict = {
        "type": token_type,
        "sub": str(user_id),
    }
    expires: timedelta = timedelta(minutes=expires_minutes)
    token: str = jwt_encoder.create_token(data=data, expires=expires)
    return token


def get_access_token(user_id: int, jwt_encoder: JwtEncoderBase) -> str:
    exp: int =config.auth.access_expires_minutes
    token_type: TokenTypeEnum = TokenTypeEnum.ACCESS
    return create_token(
        jwt_encoder=jwt_encoder,
        expires_minutes=exp,
        user_id=user_id,
        token_type=token_type
    )


def get_refresh_token(user_id: int, jwt_encoder: JwtEncoderBase) -> str:
    exp: int = config.auth.refresh_expires_minutes
    token_type: TokenTypeEnum = TokenTypeEnum.REFRESH
    return create_token(
        jwt_encoder=jwt_encoder,
        expires_minutes=exp,
        user_id=user_id,
        token_type=token_type
    )


def get_tokens_pair(user_id: int, jwt_encoder: JwtEncoderBase) -> TokenDTO:
    """
    Генерирует пару access и refresh токенов
    Returns:
        TokenDto
    """
    access_token: str = get_access_token(user_id=user_id, jwt_encoder=jwt_encoder)
    refresh_token: str = get_refresh_token(user_id=user_id, jwt_encoder=jwt_encoder)
    return TokenDTO(access_token=access_token, refresh_token=refresh_token)


def is_token_expired(payload: dict) -> bool:
    now_utc: datetime = datetime.now(timezone.utc)
    expires_timestamp: float | None = payload.get("exp")

    if not expires_timestamp:
        raise JwtExpiresNotPassedError

    return expires_timestamp < now_utc.timestamp()
