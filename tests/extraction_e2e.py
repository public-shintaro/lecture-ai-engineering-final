import os
import time
from pathlib import Path

import boto3
import pytest
import requests

# --- Service Endpoints (コンテナ間の通信用にサービス名を使用) ---
EXTRACTION_API_URL = "http://extraction:8000"
UPLOAD_API_URL = (
    "http://upload_service:8000/api/v1/upload"  # upload_serviceのコンテナ内ポートは8000
)

# --- LocalStack Configuration ---
LOCALSTACK_ENDPOINT_URL = "http://localstack:4566"
AWS_REGION = "ap-northeast-1"
VECTOR_TABLE_NAME = os.environ.get("VECTOR_TABLE_NAME", "lecture-vector-store-dev")


@pytest.fixture(scope="module")
def dynamodb_resource():
    """DynamoDBリソースをテスト全体で共有するためのpytestフィクスチャ"""
    return boto3.resource(
        "dynamodb", endpoint_url=LOCALSTACK_ENDPOINT_URL, region_name=AWS_REGION
    )


def test_extraction_service_health_check():
    """
    extraction_serviceの/healthエンドポイントが正常に応答するかをテスト
    """
    try:
        url = f"{EXTRACTION_API_URL}/health"
        print(f"Pinging health check at: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        assert response.json() == {"status": "ok"}
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the extraction service at {url}. Error: {e}")


def test_upload_and_extraction_pipeline(dynamodb_resource):
    """
    ファイルアップロードからDynamoDBへの格納までの一連のパイプラインをテスト
    """
    # 修正点: ここでslide_idを生成しない
    sample_file_path = Path(__file__).parent / "test_sample.pptx"
    assert sample_file_path.exists(), f"Sample file not found at {sample_file_path}"

    slide_id_from_server = None  # サーバーから受け取るIDを格納する変数
    try:
        with open(sample_file_path, "rb") as f:
            files = {
                "file": (
                    sample_file_path.name,
                    f,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            }
            print(f"Uploading file to: {UPLOAD_API_URL}")
            # 修正点: slide_idをPOSTデータから削除
            response = requests.post(UPLOAD_API_URL, files=files)

        response.raise_for_status()
        response_json = response.json()

        # 修正点: アサーションを削除し、サーバーが生成したIDを取得する
        assert "slide_id" in response_json
        slide_id_from_server = response_json["slide_id"]
        print(
            f"📄 File uploaded successfully. Server generated slide_id: {slide_id_from_server}"
        )

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to upload file via {UPLOAD_API_URL}. Error: {e}")

    # 2. コンシューマが処理するのを待機
    print("⏳ Waiting 15 seconds for consumer to process the file...")
    time.sleep(15)

    # 3. DynamoDBを検証
    try:
        table = dynamodb_resource.Table(VECTOR_TABLE_NAME)
        # 修正点: サーバーから受け取ったIDを使ってクエリを実行
        query_response = table.query(
            IndexName="SlideIdIndex",
            KeyConditionExpression="slide_id = :sid",
            ExpressionAttributeValues={":sid": slide_id_from_server},
        )
        items = query_response.get("Items", [])
        print(
            f"📦 Found {len(items)} chunks in DynamoDB for slide_id: {slide_id_from_server}"
        )

        assert len(items) >= 2, f"Expected at least 2 chunks, but found {len(items)}"
        print(
            f"✅ E2E Test Passed: slide_id '{slide_id_from_server}' processed and verified."
        )

    except Exception as e:
        pytest.fail(f"Failed to verify data in DynamoDB. Error: {e}")
