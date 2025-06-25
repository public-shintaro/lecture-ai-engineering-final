# backend/api/v1/upload.py
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from backend.aws_clients import s3 as s3_factory
from backend.services.upload import run_upload_sync  # ← 改名した同期版

router = APIRouter(tags=["upload"])
PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


class UploadResponse(BaseModel):
    slide_id: str = Field(..., description="ハイフン無し UUID")
    s3_key: str
    chunks: int = Field(..., description="保存したチャンク数")


@router.post(
    "/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED
)
async def upload_slide(
    file: UploadFile = File(...),
    slide_id: str = Form(...),  # ← ブラウザから送られてくる
    s3_client=Depends(s3_factory),
):
    if file.content_type != PPTX_MIME:
        raise HTTPException(400, "pptx 以外は受け付けません")

    return await run_upload_sync(
        file=file,
        slide_id=slide_id,
        s3_client=s3_client,
    )
