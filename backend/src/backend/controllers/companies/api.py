from dishka.integrations.fastapi import DishkaRoute
from dishka import FromDishka
from fastapi import APIRouter

from src.backend.controllers.companies.schemas import CompanyResponseSchema, AddCompanySchema, CompanyResponse, \
    CompaniesListResponse, DeleteCompanyResponse
from src.backend.core.companies.service import CompaniesService
from src.backend.controllers.dependencies import CurrentUserDep, AdminUserDep
from src.backend.core.companies.entity import CompanyEntity
from src.backend.core.companies.dto import AddCompanyDTO


router: APIRouter = APIRouter(route_class=DishkaRoute, prefix="/companies", tags=["Компании",])


@router.post("/")
async def create_company(
        add_company_schema: AddCompanySchema,
        admin_user: AdminUserDep,
        companies_service: FromDishka[CompaniesService],
) -> CompanyResponse:
    """ Создать компанию """
    add_company_dto: AddCompanyDTO = AddCompanyDTO(
        title=add_company_schema.title,
        created_by_id=admin_user.id
    )
    created_company: CompanyEntity = await companies_service.create(add_company_dto=add_company_dto)
    created_company_schema: CompanyResponseSchema = CompanyResponseSchema.model_validate(created_company)
    return CompanyResponse(detail="ok", company=created_company_schema)


@router.get("/my")
async def get_my_companies(
        companies_service: FromDishka[CompaniesService],
        current_user: CurrentUserDep
) -> CompaniesListResponse:
    """ Получить компании, доступные текущему пользователю """
    user_companies: list[CompanyEntity] = await companies_service.get_user_companies(user=current_user)
    companies_schemas: list[CompanyResponseSchema] = [
        CompanyResponseSchema.model_validate(company)
        for company in user_companies
    ]
    return CompaniesListResponse(detail="ok", companies=companies_schemas)


@router.delete("/{company_id}")
async def delete_company(
        company_id: int,
        companies_service: FromDishka[CompaniesService],
        current_admin_user: AdminUserDep
) -> DeleteCompanyResponse:
    """ Удалить компанию """
    is_deleted: bool = await companies_service.delete(
        company_id=company_id, requesting_user=current_admin_user
    )
    return DeleteCompanyResponse(detail="ok", deleted=is_deleted)
