from dotenv import load_dotenv

from dataclasses import dataclass
from typing import Self, Final
from os import environ


@dataclass(frozen=True, slots=True)
class AppConfig:
    host: str
    port: int
    main_admin_email: str
    main_admin_password: str


@dataclass(frozen=True, slots=True)
class AuthConfig:
    secret_key: str
    algorithm: str

    access_cookie_name: str
    refresh_cookie_name: str

    access_expires_minutes: int = 20  # 20 минут
    refresh_expires_minutes: int = 60 * 24 * 30  # 30 дней


@dataclass(frozen=True, slots=True)
class PostgresqlConfig:
    user: str
    password: str
    host: str
    port: int
    database: str

    @property
    def connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"


@dataclass(frozen=True, slots=True)
class MinioConfig:
    host: str
    access_key: str
    secret_key: str
    port: int
    secure: bool

    @property
    def endpoint_url(self) -> str:
        return ("https" if self.secure else "http") + f"://{self.host}:{self.port}"


@dataclass(frozen=True, slots=True)
class Config:
    app: AppConfig
    auth: AuthConfig

    postgresql: PostgresqlConfig
    minio: MinioConfig

    @classmethod
    def load_from_env(cls) -> Self:
        app: AppConfig = AppConfig(
            host=environ["HOST"] or "127.0.0.1",
            port=int(environ["PORT"] or 8000),
            main_admin_email=environ["MAIN_ADMIN_EMAIL"],
            main_admin_password=environ["MAIN_ADMIN_PASSWORD"]
        )

        auth: AuthConfig = AuthConfig(
            secret_key=environ["SECRET_KEY"],
            algorithm=environ["ALGORITHM"],
            access_cookie_name=environ["AUTH_COOKIE_NAME"],
            refresh_cookie_name=environ["REFRESH_COOKIE_NAME"],
        )

        postgresql: PostgresqlConfig = PostgresqlConfig(
            user=environ["POSTGRES_USER"],
            password=environ["POSTGRES_PASSWORD"],
            host=environ["POSTGRES_HOST"],
            port=int(environ["POSTGRES_PORT"]),
            database=environ["POSTGRES_DATABASE"],
        )

        minio: MinioConfig = MinioConfig(
            access_key=environ["MINIO_USER"],
            secret_key=environ["MINIO_PASSWORD"],
            host=environ["MINIO_HOST"],
            port=int(environ["MINIO_PORT"]),
            secure=bool(int(environ["MINIO_SECURE"])),
        )

        return cls(
            app=app,
            auth=auth,
            postgresql=postgresql,
            minio=minio,
        )


load_dotenv()
config: Final[Config] = Config.load_from_env()
