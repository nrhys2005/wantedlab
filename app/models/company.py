from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .company_tag import CompanyTag
from ..db import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name_ko: Mapped[str | None] = mapped_column(String)
    company_name_en: Mapped[str | None] = mapped_column(String)
    company_name_ja: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company_tags: Mapped[list["CompanyTag"]] = relationship(back_populates="company", cascade="all, delete-orphan")