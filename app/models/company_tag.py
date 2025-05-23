from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"))

    company: Mapped["Company"] = relationship(back_populates="company_tags")
    tag: Mapped["Tag"] = relationship(back_populates="company_tags")

    __table_args__ = (
        UniqueConstraint("company_id", "tag_id", name="uix_company_tag"),
        {"sqlite_autoincrement": True},
    )