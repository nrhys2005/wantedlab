import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.testclient import TestClient

from app import db
from app.api.routers import register_routers
from app.db import engine, AsyncSessionLocal
from app.dependencies import get_async_db, get_async_db_readonly
from app.models.company import Company
from app.models.company_tag import CompanyTag
from app.models.tag import Tag


def create_test_app() -> FastAPI:
    app = FastAPI()
    register_routers(app)
    return app


async def get_test_async_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def get_test_async_db_readonly():
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def test_app():
    app = create_test_app()
    app.dependency_overrides[get_async_db] = get_test_async_db
    app.dependency_overrides[get_async_db_readonly] = get_test_async_db_readonly
    yield app


@pytest.fixture(scope="session")
def client(test_app: FastAPI):
    with TestClient(test_app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def db_session():
    """테스트용 SQLite 메모리 데이터베이스 세션을 제공합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)


@pytest_asyncio.fixture
async def setup_data(db_session: AsyncSession):
    """테스트용 초기 데이터를 설정합니다."""
    company1 = Company(company_name_ko="SM Entertainment Japan", company_name_ja="株式会社SM Entertainment Japan")
    company2 = Company(company_name_ko="인포뱅크", company_name_en="infobank")
    company3 = Company(company_name_ko="SM Entertainment Korea", company_name_ja="株式会社SM Entertainment Korea")

    tag1 = Tag(tag_value="태그1", tag_ko="태그_1", tag_en="tag_1", tag_ja="タグ_1")
    tag2 = Tag(tag_value="태그2", tag_ko="태그_2", tag_en="tag_2", tag_ja="タグ_2")

    db_session.add_all([company1, company2, company3, tag1, tag2])
    await db_session.flush()

    company_tag = CompanyTag(company_id=company1.id, tag_id=tag1.id)
    company_tag2 = CompanyTag(company_id=company2.id, tag_id=tag2.id)
    company_tag3 = CompanyTag(company_id=company3.id, tag_id=tag1.id)

    db_session.add_all([company_tag, company_tag2, company_tag3])
    await db_session.commit()

    companies = await db_session.execute(
        select(Company).options(
            selectinload(Company.company_tags)
        ).where(
            Company.id.in_([company1.id, company2.id, company3.id]))
    )
    companies = companies.scalars().all()

    tags = await db_session.execute(
        select(Tag).options(
            selectinload(Tag.company_tags)
        ).where(
            Tag.id.in_([tag1.id, tag2.id]))
    )
    tags = tags.scalars().all()
    return {
        "company1": companies[0],
        "company2": companies[1],
        "company3": companies[2],
        "tag1": tags[0],
        "tag2": tags[1],
    }