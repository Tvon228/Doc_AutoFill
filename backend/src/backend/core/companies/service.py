from src.backend.core.auth.services.role_privilege import RolePrivilegeService
from src.backend.core.companies.repo import CompaniesRepositoryProtocol
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.auth.exceptions import PermissionDeniedError
from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.core.common.exceptions import NotFoundError
from src.backend.core.companies.entity import CompanyEntity
from src.backend.core.companies.dto import AddCompanyDTO
from src.backend.core.users.entity import UserEntity


class CompaniesService:

    def __init__(
            self,
            session: SessionProtocol,
            companies_repo: CompaniesRepositoryProtocol
    ):
        self.session: SessionProtocol = session
        self.companies_repo: CompaniesRepositoryProtocol = companies_repo

    async def create(self, add_company_dto: AddCompanyDTO) -> CompanyEntity:
        created_company: CompanyEntity = await self.companies_repo.create(data=add_company_dto)
        await self.session.commit()
        return created_company

    async def get_user_companies(self, user: UserEntity, ) -> list[CompanyEntity]:
        return await self.companies_repo.get_by_user(user=user)

    async def delete(self, company_id: int, requesting_user: UserEntity) -> bool:
        company: CompanyEntity | None = await self.companies_repo.get_by_id(ident=company_id)
        if not company:
            raise NotFoundError
        if company.created_by_id != requesting_user.id:
            raise PermissionDeniedError
        if not RolePrivilegeService.has_privilege(requesting_user.role, UserRoleEnum.ADMIN):
            raise PermissionDeniedError

        is_deleted: bool = await self.companies_repo.delete(company_id=company_id)
        await self.session.commit()
        return is_deleted
