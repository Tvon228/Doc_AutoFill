from io import BytesIO
import zipfile

from dishka.integrations.fastapi import DishkaRoute
from starlette.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, Query
from dishka import FromDishka

from src.backend.core.templates.interfaces.template_renderer import TemplateRendererProtocol
from src.backend.core.templates.use_cases.add_template import UploadTemplateFileUseCase
from src.backend.core.templates.services.template_fields import TemplateFieldsService
from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol
from src.backend.core.templates.services.templates import TemplatesService
from src.backend.core.templates.entities import TemplateEntity
from src.backend.controllers.schemas import DetailResponse
from src.backend.core.templates.dtos import AddTemplateDTO
from src.backend.core.companies.entity import CompanyId
from src.backend.controllers.templates.schemas import (
    ResponseTemplateSchema,
    AddTemplateSchema,
    TemplateSchema,
    ResponseTemplatesSchema,
    RenderTemplateSchema
)

router: APIRouter = APIRouter(route_class=DishkaRoute, prefix="/templates", tags=["Шаблоны",])


@router.post("/")
async def create_template(
        upload_template_schema: AddTemplateSchema,
        templates_service: FromDishka[TemplatesService],
) -> ResponseTemplateSchema:
    """ Создать шаблон """
    data: AddTemplateDTO = AddTemplateDTO(
        company_id=CompanyId(upload_template_schema.company_id),
    )
    created_template: TemplateEntity = await templates_service.create_template(data=data)
    template_schema: TemplateSchema = TemplateSchema.model_validate(created_template)
    return ResponseTemplateSchema(template=template_schema)


@router.post("/{template_id}/upload")
async def upload_template(
        template_id: int,
        uploaded_file: UploadFile,
        add_template_use_case: FromDishka[UploadTemplateFileUseCase],
) -> DetailResponse:
    """ Загрузить файл шаблона """
    await add_template_use_case.execute(
        template_id=template_id,
        file_content=uploaded_file.file,
        file_name=uploaded_file.filename
    )
    return DetailResponse(detail="ok")


# @router.get("/{template_id}")
# async def get_template(
#         template_id: int,
#         templates_service: FromDishka[TemplatesService]
# ) -> DetailResponse:
#     """ Получить информацию о шаблоне """
#     template = templates_service.get
#     return {"detail": "ok"}


@router.get("/company{company_id}")
async def get_company_templates(
        company_id: int,
        templates_service: FromDishka[TemplatesService]
) -> ResponseTemplatesSchema:
    """ Получить шаблоны компании """
    templates = await templates_service.get_by_company(company_id=company_id)
    template_schemas = [TemplateSchema.model_validate(t) for t in templates]
    return ResponseTemplatesSchema(detail="ok", templates=template_schemas)


@router.get("/unique-fields")
async def get_unique_fields_by_templates(
        template_fields_service: FromDishka[TemplateFieldsService],
        template_ids: list[int] = Query(description="Список ID шаблонов"),
) -> dict:
    """
    Получить уникальные поля для указанных шаблонов.
    """
    fields = await template_fields_service.get_unique(template_ids=template_ids)
    return fields


@router.post("/render")
async def get_unique_fields_by_templates(
        templates_service: FromDishka[TemplatesService],
        template_renderer: FromDishka[TemplateRendererProtocol],
        files_storage: FromDishka[FilesStorageProtocol],
        data: RenderTemplateSchema,
        template_ids: list[int] = Query(description="Список ID шаблонов"),
) -> StreamingResponse:
    """
    Отрендерить шаблоны
    """
    rendered_files = await templates_service.render(
        data=data.data,
        template_ids=template_ids,
        template_renderer=template_renderer,
        files_storage=files_storage
    )

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for i, file in enumerate(rendered_files):
            file.seek(0)
            zipf.writestr(f"rendered_{i + 1}.docx", file.read())
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=rendered_templates.zip"
        }
    )