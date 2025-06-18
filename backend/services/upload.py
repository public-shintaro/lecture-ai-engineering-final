# backend/services/upload.py
from __future__ import annotations

import inspect
import json
import os
from datetime import datetime, timezone
from uuid import uuid4

import aioboto3

from backend.aws_clients import ddb as ddb_factory
from backend.aws_clients import s3 as s3_factory

# --- 環境変数 ------------------------------------------------------------
BUCKET = os.getenv("UPLOAD_BUCKET", "lecture-slide-files")
TABLE = "slide_chunks"
QUEUE_URL = os.getenv("EXTRACT_QUEUE_URL")  # ★ 追加
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")  # LocalStack or real
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # Region

# ------------------------------------------------------------------------


async def _read_bytes(obj) -> bytes:
    data = obj.read()
    if inspect.isawaitable(data):  # UploadFile.read() は coroutine
        data = await data
    return data


async def _send_extract_message(slide_id: str, s3_key: str) -> None:
    """SQS へ抽出ジョブを投げる"""
    if not QUEUE_URL:  # env が無い場合はスキップ
        return

    session = aioboto3.Session()
    async with session.client(
        "sqs", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION
    ) as sqs:
        await sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(
                {
                    "slide_id": slide_id,
                    "s3_key": s3_key,
                }
            ),
            # テストが期待する MessageAttributes
            MessageAttributes={
                "slide_id": {"DataType": "String", "StringValue": slide_id},
                "bucket": {"DataType": "String", "StringValue": BUCKET},
                "s3_key": {"DataType": "String", "StringValue": s3_key},
            },
        )


async def run_upload(file_obj, *, s3_client=None, ddb_client=None) -> dict:
    """
    1. bytes を読み出し
    2. S3 put_object
    3. DynamoDB put_item (ダミー1行)
    4. SQS メッセージ送信
    5. メタ JSON を返却
    """
    s3 = s3_client or s3_factory()
    ddb = ddb_client or ddb_factory()
    table = ddb.Table(TABLE)

    slide_id = uuid4().hex
    key = f"{slide_id}/{getattr(file_obj, 'filename', 'upload.bin')}"

    body = await _read_bytes(file_obj)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body)

    table.put_item(
        Item={
            "slide_id": slide_id,
            "chunk_id": "c0000",
            "page": 0,
            "text": "dummy",
        }
    )

    # 追加: SQS へ通知
    await _send_extract_message(slide_id, key)

    return {
        "slide_id": slide_id,
        "s3_key": key,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
