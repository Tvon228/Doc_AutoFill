from dataclasses import dataclass
from typing import NewType

from src.backend.core.users.entity import UserId


CompanyId = NewType("CompanyId", int)


@dataclass(slots=True, frozen=True)
class CompanyEntity:
    id: CompanyId
    title: str
    created_by_id: UserId
