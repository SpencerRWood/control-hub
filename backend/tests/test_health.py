from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.mark.anyio
async def test_health(async_client):
    r = await async_client.get("/health/api_health")
    assert r.status_code == 200