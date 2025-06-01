from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.backend.infrastructure.db.common.base_model import BaseModel
from src.backend.infrastructure.db.common.custom_types import AutoIntPK


class CompanyModel(BaseModel):
    __tablename__ = "companies"

    id: Mapped[AutoIntPK]
    title: Mapped[str] = mapped_column(String(128))

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped["UserModel"] = relationship(back_populates="companies")
