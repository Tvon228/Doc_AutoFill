from sqlalchemy import ForeignKey, String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.infrastructure.db.common.custom_types import AutoIntPK
from src.backend.infrastructure.db.common.base_model import BaseModel
from src.backend.core.templates.enums import FieldDataTypeEnum, FieldTypeEnum


class TemplateFieldModel(BaseModel):
    __tablename__ = "template_fields"

    id: Mapped[AutoIntPK]
    name: Mapped[str] = mapped_column(String(150))
    field_type: Mapped[FieldTypeEnum] = mapped_column(Enum(FieldTypeEnum), nullable=False)
    data_type: Mapped[FieldDataTypeEnum] = mapped_column(Enum(FieldDataTypeEnum), nullable=False)

    template_id: Mapped[int] = mapped_column(
        ForeignKey(column="templates.id", ondelete="CASCADE"),
        nullable=False
    )
    template: Mapped["TemplateModel"] = relationship(back_populates="fields")

    __table_args__ = (
        UniqueConstraint("name", "template_id"),
    )
