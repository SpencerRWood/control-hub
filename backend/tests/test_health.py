import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.anyio
async def test_health(async_client):
    r = await async_client.get("/health/api")
    assert r.status_code == 200