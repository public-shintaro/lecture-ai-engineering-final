import os
import time
import uuid  # ★ slide_id を生成
from pathlib import Path

import boto3
import pytest
import requests
from boto3.dynamodb.conditions import Key  # ★ GSI への問い合わせで使用

# --- Service Endpoints ---
EXTRACTION_API_URL = os.getenv("EXTRACTION_API_URL", "http://extraction:8080")
UPLOAD_API_URL = os.getenv(
    # ★ 新しいエンドポイント (/upload) に合わせる
    "UPLOAD_API_URL",
    "http://upload_service:8000/api/v1/upload",
)

# --- LocalStack Configuration ---
DB_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL") or None
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
VECTOR_TABLE_NAME = os.getenv("VECTOR_TABLE_NAME", "slide_chunks")


@pytest.fixture(scope="module")
def dynamodb_resource():
    """pytest 全体で共有する DynamoDB リソース"""
    return boto3.resource(
        "dynamodb",
        endpoint_url=DB_ENDPOINT_URL,
        region_name=AWS_REGION,
    )


# -------------------------------------------------
# 1) Extraction Service のヘルスチェック
# -------------------------------------------------
def test_extraction_service_health_check():
    url = f"{EXTRACTION_API_URL}/api/v1/health"  # ★ /api/v1/health → /health
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        assert resp.json() == {"status": "ok"}
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Health check failed at {url}: {e}")


# -------------------------------------------------
# 2) E2E: Upload → Extract → Embed → DynamoDB
# -------------------------------------------------
def test_upload_and_extraction_pipeline(dynamodb_resource):
    sample_file = Path(__file__).parent / "test_sample.pptx"
    assert sample_file.exists(), "Sample PPTX が見つかりません"

    # ★ Upload API が要求する slide_id を生成
    slide_id = uuid.uuid4().hex

    # --- ファイルをアップロード ---
    with sample_file.open("rb") as f:
        files = {
            "file": (
                sample_file.name,
                f,
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        }
        data = {"slide_id": slide_id}  # ★ form で送信
        resp = requests.post(UPLOAD_API_URL, files=files, data=data)
    resp.raise_for_status()
    resp_json = resp.json()
    assert resp_json["slide_id"] == slide_id
    chunk_count = resp_json.get("chunks", 0)
    assert chunk_count > 0
    print(f"📤 Upload OK. chunks={chunk_count}")

    # --- 処理完了待ち（簡易） ---
    time.sleep(15)

    # --- DynamoDB で検証 ---
    table = dynamodb_resource.Table(VECTOR_TABLE_NAME)
    result = table.query(
        KeyConditionExpression=Key("slide_id").eq(slide_id),
    )
    items = result.get("Items", [])
    print(f"📦 DynamoDB items={len(items)} for slide_id={slide_id}")
    assert len(items) == chunk_count
