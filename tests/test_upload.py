import io
import os
import uuid

import requests  # anyio, httpxの代わりにrequestsを使用

# anyioマーカーは不要
# import pytest

# FastAPIのappオブジェクトは直接インポートしない

# APIサーバーのURLを環境変数から取得
# CIで設定する（ローカルテストでは手動で設定）
BASE_URL = os.getenv("UPLOAD_API_URL", "http://localhost:8001")
API_URL = f"{BASE_URL}/api/upload"


def test_upload_success():
    """正常なPPTXファイルをアップロードした場合のテスト"""
    dummy_pptx_content = b"PK\x03\x04" + b"\x00" * 100  # ZIP形式の最小ヘッダー

    # requestsで送信するためのファイル形式に整える
    files = {
        "file": (
            "demo.pptx",
            io.BytesIO(dummy_pptx_content),  # ファイルの内容
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # MIMEタイプ
        )
    }

    response = requests.post(API_URL, files=files)

    assert (
        response.status_code == 201
    )  # FastAPIのデフォルトは200だが、コードでは201を返している
    data = response.json()
    assert uuid.UUID(data["slide_id"])
    assert data["filename"] == "demo.pptx"


def test_upload_reject_non_pptx():
    """PPTX以外のファイルをアップロードした場合に正しく拒否されるかのテスト"""
    files = {
        "file": (
            "bad.txt",
            b"hello world",  # ファイルの内容
            "text/plain",  # MIMEタイプ
        )
    }

    response = requests.post(API_URL, files=files)

    assert response.status_code == 400
