import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_approval_items_lifecycle(async_client: AsyncClient):
    # create
    r = await async_client.post(
        "/approvals",
        json={
            "title": "Approve agent change",
            "description": "Agent proposes config update",
            "type": "AGENT_CONFIG",
            "payload_json": {"k": "v"},
            "requested_by": "agent:foo",
            "assigned_to": "user:spencer",
        },
    )
    assert r.status_code == 201
    item = r.json()
    item_id = item["id"]
    assert item["status"] == "PENDING"

    # list
    r = await async_client.get("/approvals", params={"status": "PENDING"})
    assert r.status_code == 200
    assert any(x["id"] == item_id for x in r.json())

    # approve
    r = await async_client.post(f"/approvals/{item_id}/approve", json={"decision_by": "user:spencer"})
    assert r.status_code == 200
    approved = r.json()
    assert approved["status"] == "APPROVED"
    assert approved["decision_by"] == "user:spencer"
    assert approved["decision_at"] is not None

    # fetch
    r = await async_client.get(f"/approvals/{item_id}")
    assert r.status_code == 200
    fetched = r.json()
    assert fetched["status"] == "APPROVED"
