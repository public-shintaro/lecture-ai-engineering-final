from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["upload"])


# ---------- 出力用スキーマ ---------- #
class UploadResponse(BaseModel):
    slide_id: str = Field(..., description="ハイフン無し UUID")
    filename: str
    content_type: str


# ---------- 保存先 ---------- #
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


async def _store_locally(slide_id: str, file: UploadFile) -> None:
    """非同期でローカル保存（S3 置き換えも容易）"""
    dest = UPLOAD_DIR / f"{slide_id}.pptx"
    async with aiofiles.open(dest, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)


# ---------- ルート ---------- #
@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_slide(file: UploadFile = File(...)) -> UploadResponse:  # noqa: B008
    if file.content_type != PPTX_MIME:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="pptx ファイルのみ受け付けます",
        )
    slide_id = uuid4().hex
    await _store_locally(slide_id, file)
    return UploadResponse(
        slide_id=slide_id,
        filename=file.filename,
        content_type=file.content_type,
    )
