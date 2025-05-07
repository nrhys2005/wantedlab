from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_db, get_async_db_readonly
from app.enums import Language
from app.models.company import Company
from app.models.company_tag import CompanyTag
from app.models.tag import Tag

router = APIRouter()

@router.get("")
async def get_companies(
    lang: Language = Language.KO,
    name: str | None = None,
    tag: str | None = None,
    db: AsyncSession = Depends(get_async_db_readonly)
):
    query = select(Company).distinct()

    if name:
        name_column = getattr(Company, f"company_name_{lang.value}")
        query = query.where(name_column.ilike(f"%{name}%"))

    if tag:
        tag_column = getattr(Tag, f"tag_{lang.value}")
        query = (
            query.join(CompanyTag)
            .join(Tag)
            .where(tag_column == tag)
        )

    result = await db.execute(query)
    companies = result.scalars().all()
    return [
        {
            "id": c.id,
            "company_name_ko": c.company_name_ko,
            "company_name_en": c.company_name_en,
            "company_name_ja": c.company_name_ja
        }
        for c in companies
    ]

@router.post("/{company_id}/tags/{tag_id}", response_model=dict)
async def connect_tag_to_company(
    company_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    company = await db.execute(select(Company).where(Company.id == company_id))
    if not company.scalars().first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Company not found")

    tag = await db.execute(select(Tag).where(Tag.id == tag_id))
    if not tag.scalars().first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Tag not found")

    existing = await db.execute(
        select(CompanyTag)
        .where(CompanyTag.company_id == company_id)
        .where(CompanyTag.tag_id == tag_id)
    )
    if existing.scalars().first():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Tag already connected to company")

    company_tag = CompanyTag(company_id=company_id, tag_id=tag_id)
    db.add(company_tag)
    return {"message": "Tag connected successfully"}


@router.delete("/{company_id}/tags/{tag_id}", response_model=dict)
async def disconnect_tag_from_company(
    company_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    company_tag = await db.execute(
        select(CompanyTag)
        .where(CompanyTag.company_id == company_id)
        .where(CompanyTag.tag_id == tag_id)
    )
    company_tag = company_tag.scalars().first()
    if not company_tag:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Tag connection not found")

    await db.delete(company_tag)
    await db.flush()
    return {"message": "Tag disconnected successfully"}
