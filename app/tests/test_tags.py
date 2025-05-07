from http import HTTPStatus

import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_tag(client: TestClient, setup_data):
    # 성공: 새로운 태그 생성
    response = client.post(
        "/tags",
        json={"tag_value":"태그11", "tag_ko": "태그_11", "tag_en": "tag_11"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["tag_ko"] == "태그_11"
    assert response.json()["tag_en"] == "tag_11"

    # 실패: 중복 태그
    response = client.post(
        "/tags",
        json={"tag_value":"신규태그", "tag_ko": "태그_11"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Tag value '태그_11' already exists for tag_ko"

    # 실패: 태그 값 없음
    response = client.post(
        "/tags",
        json={"tag_value":"신규태그", "tag_ko": "", "tag_en": "", "tag_ja": ""}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "At least one tag value (tag_ko, tag_en, tag_ja) is required"

@pytest.mark.asyncio
async def test_update_tag(client: TestClient, setup_data):
    # 성공: 태그 수정
    response = client.put(
        "/tags/1",
        json={"tag_ko": "태그_수정"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["tag_ko"] == "태그_수정"

    # 실패: 존재하지 않는 태그
    response = client.put(
        "/tags/999",
        json={"tag_ko": "태그_수정"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Tag not found"

    # 실패: 중복 태그 값
    response = client.put(
        "/tags/2",
        json={"tag_ko": "태그_수정"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Tag value '태그_수정' already exists for tag_ko"

@pytest.mark.asyncio
async def test_delete_tag(client: TestClient, setup_data):
    # 성공: 태그 삭제
    response = client.delete("/tags/2")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Tag deleted successfully"}

    # 실패: 존재하지 않는 태그
    response = client.delete("/tags/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Tag not found"
