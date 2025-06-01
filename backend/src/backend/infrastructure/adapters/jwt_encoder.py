from datetime import timedelta, timezone, datetime

import jwt
from jwt import PyJWTError
from loguru import logger

from src.backend.core.auth.interfaces.jwt_encoder import JwtEncoderBase
from src.backend.core.auth.exceptions import JwtDecodeError


class JwtEncoder(JwtEncoderBase):

    def create_token(self, data: dict, expires: timedelta) -> str:
        expire: datetime = datetime.now(timezone.utc) + expires

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=self._key, algorithm=self._algorithm)

        return encoded_jwt

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=self._key,
                algorithms=self._algorithm,
                verify=False,
                options={"verify_exp": False}
            )
        except PyJWTError as e:
            logger.info(e)
            raise JwtDecodeError

