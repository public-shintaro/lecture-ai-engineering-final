# backend/services/upload.py
from __future__ import annotations

import inspect
from datetime import datetime, timezone
from uuid import uuid4

from backend.aws_clients import ddb as ddb_factory
from backend.aws_clients import s3 as s3_factory

BUCKET = "lecture-slide-files"
TABLE = "slide_chunks"


async def _read_bytes(obj) -> bytes:
    """UploadFile でも BytesIO でも読めるユーティリティ"""
    data = obj.read()
    if inspect.isawaitable(data):  # UploadFile.read() は coroutine
        data = await data
    return data


async def run_upload(file_obj, *, s3_client=None, ddb_client=None) -> dict:
    """
    1. bytes を読み出し
    2. S3 put_object
    3. DynamoDB put_item (ダミー1行)
    4. メタ JSON を返却
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

    return {
        "slide_id": slide_id,
        "s3_key": key,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
