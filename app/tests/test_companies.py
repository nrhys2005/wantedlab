from http import HTTPStatus

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from app.enums import Language


@pytest.mark.asyncio
async def test_get_companies(client: TestClient, setup_data):
    company1 = setup_data.get("company1")
    response = client.get("/companies")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 3
    assert response.json()[0]["id"] == company1.id
    assert response.json()[0]["company_name_ko"] == company1.company_name_ko
    assert response.json()[0]["company_name_en"] == company1.company_name_en
    assert response.json()[0]["company_name_ja"] == company1.company_name_ja

@pytest.mark.asyncio
async def test_get_companies_filter(client: TestClient, setup_data):
    company1 = setup_data.get("company1")
    company2 = setup_data.get("company2")
    company3 = setup_data.get("company3")
    tag1 = setup_data.get("tag1")
    tag2 = setup_data.get("tag2")

    # name 전체 & lang ko
    response = client.get(f"/companies?name={company1.company_name_ko}&lang={Language.KO}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company1.id

    # name 전체 & # lang en
    assert company2.company_name_en == "infobank"
    response = client.get(f"/companies?name={company2.company_name_en}&lang={Language.EN}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company2.id

    # name 전체 & # lang ja
    assert company3.company_name_ja == "株式会社SM Entertainment Korea"
    response = client.get(f"/companies?name={company3.company_name_ja}&lang={Language.JA}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company3.id

    # name 부분 & lang ko
    assert company1.company_name_ko == "SM Entertainment Japan"
    assert company3.company_name_ko == "SM Entertainment Korea"
    response = client.get(f"/companies?name=SM Entertainment&lang={Language.KO}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == company1.id
    assert response.json()[1]["id"] == company3.id

    # name 부분 & # lang en
    assert company2.company_name_en == "infobank"
    response = client.get(f"/companies?name=info&lang={Language.EN}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company2.id

    # name 부분 & # lang ja
    assert company1.company_name_ja == "株式会社SM Entertainment Japan"
    assert company3.company_name_ja == "株式会社SM Entertainment Korea"
    response = client.get(f"/companies?name=株式会社SM Entertainment&lang={Language.JA}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == company1.id
    assert response.json()[1]["id"] == company3.id

    # tag & lang ko
    assert set(tag1.company_tags) & set(company1.company_tags)
    assert set(tag1.company_tags) & set(company3.company_tags)
    response = client.get(f"/companies?tag={tag1.tag_ko}&lang={Language.KO}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == company1.id
    assert response.json()[1]["id"] == company3.id

    # tag & # lang en
    assert set(tag2.company_tags) & set(company2.company_tags)
    response = client.get(f"/companies?tag={tag2.tag_en}&lang={Language.EN}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company2.id

    # tag & # lang ja
    assert set(tag2.company_tags) & set(company2.company_tags)
    response = client.get(f"/companies?tag={tag2.tag_ja}&lang={Language.JA}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == company2.id


@pytest.mark.asyncio
async def test_connect_tag_to_company(client: TestClient, setup_data):
    company1 = setup_data.get("company1")
    tag1 = setup_data.get("tag1")

    # 성공: 태그 연결
    response = client.post("/companies/1/tags/2")
    assert response.status_code == HTTPStatus.OK

    # 실패: 존재하지 않는 회사
    response = client.post("/companies/999/tags/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Company not found"

    # 실패: 존재하지 않는 태그
    response = client.post("/companies/1/tags/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Tag not found"

    # 실패: 이미 연결된 태그
    assert set(tag1.company_tags) & set(company1.company_tags)
    response = client.post("/companies/1/tags/1")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Tag already connected to company"

@pytest.mark.asyncio
async def test_disconnect_tag_from_company(client: TestClient, db_session:AsyncSession, setup_data):
    company1 = setup_data.get("company1")
    tag1 = setup_data.get("tag1")

    # 성공: 태그 연결 해제
    assert set(tag1.company_tags) & set(company1.company_tags)
    response = client.delete("/companies/1/tags/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Tag disconnected successfully"}
    await db_session.refresh(company1, ["company_tags"])
    assert company1.company_tags == []

    # 실패: 존재하지 않는 연결
    response = client.delete("/companies/1/tags/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Tag connection not found"
