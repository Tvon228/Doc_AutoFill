from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.backend.infrastructure.db.common.custom_types import AutoIntPK
from src.backend.infrastructure.db.common.base_model import BaseModel


class TemplateModel(BaseModel):
    __tablename__ = "templates"

    id: Mapped[AutoIntPK]
    file_name: Mapped[str] = mapped_column(String(100), nullable=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE")
    )

    fields: Mapped[list["TemplateFieldModel"]] = relationship(back_populates="template")
