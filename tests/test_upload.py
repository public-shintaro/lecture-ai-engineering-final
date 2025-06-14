# tests/test_upload.py

import io
import uuid

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient  # ASGITransport をインポート

from backend.app.main import app


@pytest.mark.anyio
async def test_upload_success():
    """正常なPPTXファイルをアップロードした場合のテスト"""
    dummy_pptx_content = b"PK\x03\x04" + b"\x00" * 100  # ZIP形式の最小ヘッダー
    dummy_file = io.BytesIO(dummy_pptx_content)

    # vvv---ここから修正---vvv
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # ^^^---ここまで修正---^^^
        response = await client.post(
            "/api/upload",
            files={
                "file": (
                    "demo.pptx",
                    dummy_file,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            },
        )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert uuid.UUID(data["slide_id"])
    assert data["filename"] == "demo.pptx"


@pytest.mark.anyio
async def test_upload_reject_non_pptx():
    """PPTX以外のファイルをアップロードした場合に正しく拒否されるかのテスト"""
    # vvv---ここから修正---vvv
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # ^^^---ここまで修正---^^^
        response = await client.post(
            "/api/upload",
            files={"file": ("bad.txt", b"hello world", "text/plain")},
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
