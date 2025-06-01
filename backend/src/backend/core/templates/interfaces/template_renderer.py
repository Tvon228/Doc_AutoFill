from typing import Protocol, BinaryIO


class TemplateRendererProtocol(Protocol):

    def render(self, file: BinaryIO, data: dict) -> BinaryIO:
        ...
