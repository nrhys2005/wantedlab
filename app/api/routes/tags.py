from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.tag import TagCreate, TagResponse, TagUpdate
from app.dependencies import get_async_db
from app.models.tag import Tag

router = APIRouter()

@router.post("", response_model=TagResponse)
async def create_tag(
    tag: TagCreate,
    db: AsyncSession = Depends(get_async_db)
):
    for field in ["tag_ko", "tag_en", "tag_ja"]:
        tag_value = getattr(tag, field)
        if tag_value:
            existing_tag = await db.execute(
                select(Tag).where(getattr(Tag, field) == tag_value)
            )
            if existing_tag.scalars().first():
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Tag value '{tag_value}' already exists for {field}"
                )

    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    await db.flush()
    return db_tag

@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    tag = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = tag.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    for field, value in tag_update.dict().items():
        if value and value != getattr(tag, field):
            existing = await db.execute(
                select(Tag).where(getattr(Tag, field) == value).where(Tag.id != tag_id)
            )
            if existing.scalars().first():
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Tag value '{value}' already exists for {field}"
                )
        setattr(tag, field, value)
    await db.commit()
    return tag

@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    tag = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = tag.scalars().first()
    if not tag:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Tag not found")

    await db.delete(tag)
    return {"message": "Tag deleted successfully"}