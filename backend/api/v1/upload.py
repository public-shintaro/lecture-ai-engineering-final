from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

import aioboto3
import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["upload"])

# --- 設定 ---
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

# --- AWS接続設定 (環境変数から) ---
BUCKET = os.getenv("UPLOAD_BUCKET", "slides-upload-dev")
QUEUE_URL = os.getenv("EXTRACT_QUEUE_URL")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # リージョンも環境変数から取得


# --- レスポンススキーマ ---
class UploadResponse(BaseModel):
    slide_id: str = Field(..., description="ハイフン無し UUID")
    filename: str
    content_type: str


# --- 内部ユーティリティ ---
async def _store_locally(slide_id: str, file: UploadFile) -> None:
    dest = UPLOAD_DIR / f"{slide_id}.pptx"
    async with aiofiles.open(dest, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)


async def _upload_to_s3(slide_id: str, file: UploadFile) -> str:
    key = f"{slide_id}.pptx"
    session = aioboto3.Session()
    # vvv---ここを修正---vvv
    async with session.client(
        "s3", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION
    ) as s3:
        # ^^^---ここまで修正---^^^
        await s3.upload_fileobj(
            file.file, BUCKET, key, ExtraArgs={"ContentType": file.content_type}
        )
    return key


async def _send_extract_message(slide_id: str, s3_key: str) -> None:
    if not QUEUE_URL:
        return

    session = aioboto3.Session()
    # vvv---ここを修正---vvv
    async with session.client(
        "sqs", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION
    ) as sqs:
        # ^^^---ここまで修正---^^^
        await sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody="extract",
            MessageAttributes={
                "slide_id": {"StringValue": slide_id, "DataType": "String"},
                "bucket": {"StringValue": BUCKET, "DataType": "String"},
                "s3_key": {"StringValue": s3_key, "DataType": "String"},
            },
        )


# --- ルーター ---
@router.post(
    "/v1/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_slide(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != PPTX_MIME:
        raise HTTPException(status_code=400, detail="pptx 以外は受け付けません")

    slide_id = uuid4().hex

    await _store_locally(slide_id, file)
    await file.seek(0)

    s3_key = await _upload_to_s3(slide_id, file)
    await _send_extract_message(slide_id, s3_key)

    return UploadResponse(
        slide_id=slide_id,
        filename=file.filename,
        content_type=file.content_type,
    )
