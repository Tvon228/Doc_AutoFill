from typing import BinaryIO
from io import BytesIO

from docxtpl import DocxTemplate
from src.backend.core.templates.interfaces.template_renderer import TemplateRendererProtocol


class TemplateRenderer(TemplateRendererProtocol):
    def render(self, file: BinaryIO, data: dict) -> BinaryIO:
        template = DocxTemplate(file)
        template.render(context=data)

        output = BytesIO()
        template.save(output)
        return output
