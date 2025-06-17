import io

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture()
def client(monkeypatch):
    async def fake_run_upload(file_obj, *, s3_client=None, ddb_client=None):
        return {"slide_id": "stub", "s3_key": "dummy/key"}

    # ① service 層
    monkeypatch.setattr(
        "backend.services.upload.run_upload", fake_run_upload, raising=True
    )
    # ② ルーター層（upload.py が名前付き import した実体）
    monkeypatch.setattr(
        "backend.api.v1.upload.run_upload", fake_run_upload, raising=True
    )

    return TestClient(app)


def test_upload_endpoint(client):
    file = io.BytesIO(b"dummy")
    file.filename = "x.pptx"
    resp = client.post(
        "/api/v1/document/embed",
        files={
            "file": (
                "x.pptx",
                file,
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        },
    )
    assert resp.status_code == 201
    assert resp.json()["slide_id"] == "stub"
