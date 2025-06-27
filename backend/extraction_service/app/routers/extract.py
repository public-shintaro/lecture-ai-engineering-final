# backend/extraction_service/app/routers/extract.py
"""
/extract ルータ
- アップロードされた PPTX を受け取り
- parser.parse_pptx_to_texts() で各スライドのテキストを抽出
- チャンク（スライド単位 or 1500 文字分割）を S3 に保存
- [{idx, s3_key}, ...] を返す
"""

from __future__ import annotations

import os
from typing import List

from app.services.parser import parse_pptx_to_texts
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from backend.aws_clients import s3 as s3_factory

router = APIRouter(tags=["extract"])

PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
CHUNK_BUCKET = os.getenv("CHUNK_BUCKET", "lecture-slide-chunks")
MAX_CHARS = int(os.getenv("CHUNK_MAX_CHARS", "1500"))


class ChunkMeta(BaseModel):
    idx: int = Field(0, description="チャンク番号 (0 origin)")
    page: int = Field(..., description="元スライドのページ番号 (1 origin)")
    s3_key: str = Field(..., description="S3 オブジェクトキー")


def _split_long_text(text: str, max_chars: int) -> List[str]:
    """max_chars でテキストを分割しリストで返す"""
    if len(text) <= max_chars:
        return [text]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


@router.post(
    "/extract",
    response_model=List[ChunkMeta],
    status_code=status.HTTP_201_CREATED,
)
async def extract_slide(
    file: UploadFile = File(...),
    slide_id: str = Form(...),
    s3_client=Depends(s3_factory),
):
    # ---- MIME チェック ----
    if file.content_type != PPTX_MIME:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="pptx 以外は受け付けません"
        )

    # ---- テキスト抽出 ----
    try:
        raw_bytes = await file.read()
        slide_texts = parse_pptx_to_texts(raw_bytes)  # List[str]
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"pptx parse error: {e}"
        )

    # ---- チャンク化＋S3保存 ----
    metas: List[ChunkMeta] = []
    idx = 0
    for page_no, slide_text in enumerate(slide_texts, start=1):
        for chunk in _split_long_text(slide_text, MAX_CHARS):
            key = f"{slide_id}/chunk_{idx:03d}.txt"
            s3_client.put_object(
                Bucket=CHUNK_BUCKET,
                Key=key,
                Body=chunk.encode("utf-8"),
                ContentType="text/plain",
            )
            metas.append(ChunkMeta(idx=idx, page=page_no, s3_key=key))
            idx += 1

    return metas
