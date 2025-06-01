from typing import List

from pydantic import BaseModel


class AddCompanySchema(BaseModel):
    title: str


class CompanyResponseSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True



class CompanyResponse(BaseModel):
    detail: str
    company: CompanyResponseSchema


class CompaniesListResponse(BaseModel):
    detail: str
    companies: List[CompanyResponseSchema]


class DeleteCompanyResponse(BaseModel):
    detail: str
    deleted: bool
