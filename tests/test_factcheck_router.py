import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture()
def client(monkeypatch):
    async def fake(slide_id, **_):
        return {"slide_id": slide_id, "issues": []}

    # 両方差し替え
    monkeypatch.setattr("backend.services.factcheck.run_factcheck", fake, raising=True)
    monkeypatch.setattr("backend.api.v1.factcheck.run_factcheck", fake, raising=True)
    return TestClient(app)


def test_factcheck_endpoint(client):
    res = client.post("/api/v1/factcheck", json={"slide_id": "demo"})
    assert res.status_code == 201
    assert res.json()["slide_id"] == "demo"
