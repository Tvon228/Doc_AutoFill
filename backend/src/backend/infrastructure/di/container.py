from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.backend.infrastructure.di.providers.auth.auth_service import AuthServiceProvider
from src.backend.infrastructure.di.providers.auth.password_hasher import PasswordHasherProvider
from src.backend.infrastructure.di.providers.auth.jwt_encoder import JwtEncoderProvider
from src.backend.infrastructure.di.providers.common.files_storage import FilesStorageProvider
from src.backend.infrastructure.di.providers.companies.companies_repo import CompaniesRepositoryProvider
from src.backend.infrastructure.di.providers.companies.companies_service import CompaniesServiceProvider
from src.backend.infrastructure.di.providers.templates.add_template_use_case import AddTemplateUseCaseProvider
from src.backend.infrastructure.di.providers.templates.template_fields_repo import TemplateFieldsRepositoryProvider
from src.backend.infrastructure.di.providers.templates.template_fields_service import TemplateFieldsServiceProvider
from src.backend.infrastructure.di.providers.templates.template_parser import TemplateParserFactoryProvider
from src.backend.infrastructure.di.providers.templates.template_renderer import TemplateRendererProvider
from src.backend.infrastructure.di.providers.templates.templates_repo import TemplatesRepositoryProvider
from src.backend.infrastructure.di.providers.templates.templates_service import TemplatesServiceProvider
from src.backend.infrastructure.di.providers.users.users_repo import UsersRepoProvider
from src.backend.infrastructure.di.providers.common.session import SessionProvider
from src.backend.main.config import (
    Config,
    PostgresqlConfig,
    AuthConfig,
    MinioConfig
)
from src.backend.infrastructure.di.providers.users.users_service import UsersServiceProvider


def get_async_container(config: Config) -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        # common
        SessionProvider(),
        FilesStorageProvider(),
        # users
        UsersRepoProvider(),
        UsersServiceProvider(),
        # auth
        JwtEncoderProvider(),
        PasswordHasherProvider(),
        AuthServiceProvider(),
        # companies
        CompaniesRepositoryProvider(),
        CompaniesServiceProvider(),
        # templates
        TemplateParserFactoryProvider(),
        TemplateRendererProvider(),
        TemplatesRepositoryProvider(),
        TemplatesServiceProvider(),
        TemplateFieldsRepositoryProvider(),
        TemplateFieldsServiceProvider(),
        AddTemplateUseCaseProvider(),

        context={
            AuthConfig: config.auth,
            PostgresqlConfig: config.postgresql,
            MinioConfig: config.minio,
        },
    )