from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, model_validator, Field


class TagCreate(BaseModel):
    tag_value:str = Field(..., min_length=1)
    tag_ko: str | None = None
    tag_en: str | None = None
    tag_ja: str | None = None

    @model_validator(mode="after")
    def check_at_least_one_tag_value(cls, values):
        if not any([values.tag_ko, values.tag_en, values.tag_ja]):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="At least one tag value (tag_ko, tag_en, tag_ja) is required"
            )
        return values


class TagUpdate(BaseModel):
    tag_ko: str | None = None
    tag_en: str | None = None
    tag_ja: str | None = None

    @model_validator(mode="after")
    def check_at_least_one_tag_value(cls, values):
        if not any([values.tag_ko, values.tag_en, values.tag_ja]):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="At least one tag value (tag_ko, tag_en, tag_ja) is required"
            )
        return values


class TagResponse(BaseModel):
    id: int
    tag_ko: str | None = None
    tag_en: str | None = None
    tag_ja: str | None = None

    class Config:
        from_attributes = True
