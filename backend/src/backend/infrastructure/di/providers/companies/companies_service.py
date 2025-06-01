from dishka import Provider, Scope, provide

from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.companies.repo import CompaniesRepositoryProtocol
from src.backend.core.companies.service import CompaniesService


class CompaniesServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_companies_service(
            self,
            companies_repo: CompaniesRepositoryProtocol,
            session: SessionProtocol,
    ) -> CompaniesService:
        return CompaniesService(
            session=session,
            companies_repo=companies_repo,
        )
