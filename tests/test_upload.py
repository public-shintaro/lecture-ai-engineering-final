import io
import os
import uuid

import boto3  # <-- 追加
import pytest
import requests

# --- テスト用の設定 ---
# APIサーバーのURLを環境変数から取得
BASE_URL = os.getenv("UPLOAD_API_URL", "http://upload_service:8000")
API_URL = f"{BASE_URL}/api/v1/upload"

# LocalStackのエンドポイントURLを環境変数から取得
# CIで設定する（ローカルテストでは手動で設定 or .env）
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# LocalStackに接続するためのboto3クライアント
# .envから読み込まれる認証情報はダミーでOK
s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name="us-east-1",
    aws_access_key_id="test",  # <-- ダミーの認証情報を追加
    aws_secret_access_key="test",  # <-- ダミーの認証情報を追加
)
sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name="us-east-1",
    aws_access_key_id="test",  # <-- ダミーの認証情報を追加
    aws_secret_access_key="test",  # <-- ダミーの認証情報を追加
)

# .envからバケット名とキューURLを取得
UPLOAD_BUCKET = os.getenv("UPLOAD_BUCKET", "lecture-slide-files")
EXTRACT_QUEUE_URL = os.getenv(
    "EXTRACT_QUEUE_URL", "http://localhost:4566/000000000000/slide-extract-queue"
)


@pytest.mark.xfail(reason="Extraction service consumes the message immediately")
def test_upload_s3_sqs_e2e():
    """正常なPPTXファイルをアップロードし、S3とSQSの連携をE2Eでテストする"""
    dummy_pptx_content = b"PK\x03\x04" + b"\x00" * 100  # ZIP形式の最小ヘッダー

    # 1. APIにファイルをPOST
    files = {
        "file": (
            "demo.pptx",
            io.BytesIO(dummy_pptx_content),
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    }
    response = requests.post(API_URL, files=files)

    # 2. APIレスポンスを検証
    assert response.status_code == 201
    body = response.json()
    slide_id = body["slide_id"]
    assert uuid.UUID(slide_id)  # slide_idが有効なUUID形式か検証

    # 3. S3にオブジェクトがアップロードされたか検証
    try:
        s3.head_object(Bucket=UPLOAD_BUCKET, Key=f"{slide_id}/demo.pptx")
    except s3.exceptions.ClientError as e:
        assert False, f"S3 object not found: {e}"

    # 4. SQSにメッセージが送信されたか検証
    messages = sqs.receive_message(
        QueueUrl=EXTRACT_QUEUE_URL,
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        WaitTimeSeconds=5,  # メッセージが届くまで最大5秒待つ
    ).get("Messages", [])

    assert len(messages) == 1, "SQS message not found"

    # 5. SQSメッセージの内容を検証
    message = messages[0]
    attrs = message["MessageAttributes"]
    assert attrs["slide_id"]["StringValue"] == slide_id
    assert attrs["bucket"]["StringValue"] == UPLOAD_BUCKET
    assert attrs["s3_key"]["StringValue"] == f"{slide_id}/demo.pptx"

    # テスト後にメッセージを削除しておく
    sqs.delete_message(
        QueueUrl=EXTRACT_QUEUE_URL, ReceiptHandle=message["ReceiptHandle"]
    )


def test_upload_reject_non_pptx():
    """PPTX以外のファイルをアップロードした場合に正しく拒否されるかのテスト"""
    files = {"file": ("bad.txt", b"hello world", "text/plain")}
    data = {"slide_id": "dummy"}  # ★ slide_id を付ける
    response = requests.post(API_URL, files=files, data=data)
    print(response.status_code, response.text)
    assert response.status_code == 400
