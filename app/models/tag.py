from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_value: Mapped[str] = mapped_column(String)
    tag_ko: Mapped[str | None] = mapped_column(String)
    tag_en: Mapped[str | None] = mapped_column(String)
    tag_ja: Mapped[str | None] = mapped_column(String)

    company_tags: Mapped[list["CompanyTag"]] = relationship(back_populates="tag", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("tag_ko", name="uq_tag_ko", postgresql_nulls_not_distinct=True),
        UniqueConstraint("tag_en", name="uq_tag_en", postgresql_nulls_not_distinct=True),
        UniqueConstraint("tag_ja", name="uq_tag_ja", postgresql_nulls_not_distinct=True),
    )