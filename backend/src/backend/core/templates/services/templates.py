from typing import BinaryIO

from src.backend.core.templates.interfaces.template_renderer import TemplateRendererProtocol
from src.backend.core.templates.repositories.templates import TemplatesRepositoryProtocol
from src.backend.core.common.interfaces.files_storage import FilesStorageProtocol
from src.backend.core.templates.entities import TemplateEntity, TemplateId
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.templates.exceptions import InvalidFileError
from src.backend.core.common.exceptions import NotFoundError
from src.backend.core.templates.dtos import AddTemplateDTO


class TemplatesService:

    def __init__(self, session: SessionProtocol, templates_repo: TemplatesRepositoryProtocol):
        self.session: SessionProtocol = session
        self.templates_repo: TemplatesRepositoryProtocol = templates_repo
        self._files_category = "templates"

    @staticmethod
    def __get_extension(file_name: str) -> str:
        return file_name.rsplit(sep=".", maxsplit=1)[-1]

    @classmethod
    def __get_file_key(cls, template_id: int, file_name: str) -> str:
        file_extension: str = cls.__get_extension(file_name=file_name)
        filename: str = f"{template_id}.{file_extension}"
        return filename

    async def get(self, ident: TemplateId) -> TemplateEntity | None:
        template: TemplateEntity | None = await self.templates_repo.get(ident=ident)
        return template

    async def create_template(self, data: AddTemplateDTO) -> TemplateEntity:
        # Сохраняем в БД
        template: TemplateEntity = await self.templates_repo.add(data=data)
        await self.session.commit()
        return template

    async def upload(
            self,
            template_id: int,
            file_name: str,
            file_content: BinaryIO,
            files_storage: FilesStorageProtocol,
    ) -> bool:
        # Пока поддерживаются только эти
        if self.__get_extension(file_name) not in ("doc", "docx"):
            raise InvalidFileError

        template: TemplateEntity = await self.get(ident=TemplateId(template_id))
        if not template:
            raise NotFoundError

        await self.templates_repo.set_file_name(template_id=template_id, file_name=file_name)
        await self.session.commit()

        file_key: str = self.__get_file_key(template_id=template_id, file_name=file_name)
        await files_storage.save(category=self._files_category, filename=file_key, content=file_content)
        return True

    async def get_by_company(self, company_id: int) -> list[TemplateEntity]:
        return await self.templates_repo.get_by_company(company_id=company_id)

    async def render(
            self,
            template_ids: list[int],
            data: dict,
            template_renderer: TemplateRendererProtocol,
            files_storage: FilesStorageProtocol,
    ) -> list[BinaryIO]:
        rendered_files: list[BinaryIO] = []
        template_ids: list[TemplateId] = [TemplateId(t_id) for t_id in template_ids]
        templates: list[TemplateEntity] = await self.templates_repo.get_by_ids(template_ids=template_ids)

        for template in templates:
            file_key: str = self.__get_file_key(template_id=template.id, file_name=template.file_name)
            file: BinaryIO = await files_storage.get(category=self._files_category, filename=file_key)
            rendered_file: BinaryIO = template_renderer.render(file=file, data=data)
            rendered_files.append(rendered_file)

        return rendered_files
