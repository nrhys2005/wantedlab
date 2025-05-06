from pydantic import BaseModel

class TagCreate(BaseModel):
    tag_ko: str
    tag_en: str
    tag_ja: str

    class Config:
        from_attributes = True

class TagUpdate(BaseModel):
    tag_ko: str | None = None
    tag_en: str | None = None
    tag_ja: str | None = None

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    id: int
    tag_ko: str | None
    tag_en: str | None
    tag_ja: str | None

    class Config:
        from_attributes = True