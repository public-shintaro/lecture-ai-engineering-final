# backend/api/v1/upload.py
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from backend.aws_clients import ddb as ddb_factory
from backend.aws_clients import s3 as s3_factory
from backend.services.upload import run_upload

router = APIRouter(tags=["upload"])
PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


class UploadResponse(BaseModel):
    slide_id: str = Field(..., description="ハイフン無し UUID")
    s3_key: str


@router.post(
    "/document/embed",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_slide(
    file: UploadFile = File(...),
    s3_client=Depends(s3_factory),
    ddb_client=Depends(ddb_factory),
):
    if file.content_type != PPTX_MIME:
        raise HTTPException(400, "pptx 以外は受け付けません")

    return await run_upload(file, s3_client=s3_client, ddb_client=ddb_client)
