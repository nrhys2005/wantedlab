from fastapi import FastAPI

from app.api.routes import companies, tags


def register_routers(app: FastAPI) -> None:
    """
    FastAPI 앱에 모든 라우터를 등록합니다.
    """
    app.include_router(companies.router, prefix="/companies", tags=["companies"])
    app.include_router(tags.router, prefix="/tags", tags=["tags"])
