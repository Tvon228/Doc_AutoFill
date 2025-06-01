from datetime import datetime

from sqlalchemy import String, BigInteger, Enum, DateTime, func, ForeignKey, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.infrastructure.db.common.base_model import BaseModel
from src.backend.infrastructure.db.common.custom_types import AutoIntPK


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[AutoIntPK]
    name: Mapped[str] = mapped_column(String(80))

    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), default=UserRoleEnum.EMPLOYEE)
    added_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )

    password_hash: Mapped[str] = mapped_column(String(128))
    email: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    phone: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    companies: Mapped["CompanyModel"] = relationship(back_populates="created_by")

    added_by: Mapped["UserModel"] = relationship(
        "UserModel",
        remote_side="UserModel.id",
        back_populates="added_users"
    )

    added_users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="added_by"
    )
