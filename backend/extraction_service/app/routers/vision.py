import logging

from fastapi import APIRouter, File, UploadFile
from models import VisionAnalysisResult

# 修正: 呼び出す関数名を変更
from services.vision import analyze_image_with_model

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/vision",
    response_model=VisionAnalysisResult,
    summary="Analyze a Slide Image",
    tags=["Vision"],
)
async def create_vision_analysis(file: UploadFile = File(...)):
    """
    Upload a slide image (PNG, JPEG) to get a fact-check and source suggestions.
    """
    image_bytes = await file.read()
    # 修正: 呼び出す関数名を変更
    analysis_result = analyze_image_with_model(image_bytes)
    return analysis_result


# Contains AI-generated edits.
