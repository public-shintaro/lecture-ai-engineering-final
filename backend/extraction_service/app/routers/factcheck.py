import logging

from fastapi import APIRouter, HTTPException
from models import Inconsistency
from services.factcheck import factcheck_slide

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/factcheck", tags=["Fact-Checking"])


@router.get("/{slide_id}", response_model=list[Inconsistency])
async def get_factcheck_for_slide(slide_id: str):
    """
    指定されたスライドIDに対してファクトチェックを実行し、矛盾点のリストを返す。
    """
    logger.info(f"Received fact-check request for slide_id: {slide_id}")
    try:
        # サービス層のロジックを呼び出す
        inconsistencies = factcheck_slide(slide_id)
        return inconsistencies
    except Exception:
        logger.exception(
            f"An unexpected error occurred during fact-checking for slide_id {slide_id}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred while fact-checking slide {slide_id}.",
        )
