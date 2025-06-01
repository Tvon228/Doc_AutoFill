from typing import Protocol, IO


class EmailSenderProtocol(Protocol):
    async def send(
        self,
        content: str | IO,
        from_: str,
        to: str,
        subject: str | None = None,
        attachments: list[IO] | None = None
    ) -> bool: ...


class SmsSenderProtocol(Protocol):
    async def send(
        self,
        content: str,
        to: str,
        flash: bool = False
    ) -> bool: ...
