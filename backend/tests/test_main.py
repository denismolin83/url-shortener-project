import pytest
import pytest_asyncio

async def test_create_url(client):
    payload = {"target_url": "https://python.org"}
    response = await client.post("/api/shorten", json=payload)

    if response.status_code == 422:
        print(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["original_url"] == "https://python.org/"
    assert "short_key" in data
    assert len(data["short_key"]) == 5


async def test_redirect_url(client):
    payload = {"target_url": "https://fastapi.tiangolo.com"}
    res_create = await client.post("/api/shorten", json=payload)
    key = res_create.json()["short_key"]

    response = await client.get(f"/api/{key}")

    assert response.status_code == 307
    assert response.headers["location"] == "https://fastapi.tiangolo.com/"


async def test_duplicate_url(client):
    #тесть на то, что для одной ссылки возвращается один и тот же ключ
    payload = {"target_url": "https://google.com"}

    res1 = await client.post("/api/shorten", json=payload)
    res2 = await client.post("/api/shorten", json=payload)
    
    assert res1.json()["short_key"] == res2.json()["short_key"]


async def test_not_found_url(client):
    response = await client.get("/api/nonexistent")
    assert response.status_code == 404