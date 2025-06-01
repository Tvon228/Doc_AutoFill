from dataclasses import dataclass

from src.backend.core.users.entity import UserId


@dataclass(frozen=True, slots=True)
class AddCompanyDTO:
    title: str
    created_by_id: UserId
