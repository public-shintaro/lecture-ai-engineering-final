import logging
import tempfile
from pathlib import Path
from typing import List

# 高レベルな関数ではなく、PptxLoaderを直接インポートします
from exparso.loader.pptx_loader import PptxLoader

# PptxLoaderが返すオブジェクトの型もインポートします
from exparso.model import LoadPageContents
from fastapi import UploadFile

logger = logging.getLogger(__name__)


def extract_text_from_pptx(file: UploadFile) -> List[str]:
    """
    Extracts text from each slide of an uploaded PPTX file by directly using the exparso.PptxLoader.
    """
    texts: List[str] = []
    tmp_path = ""
    try:
        # アップロードされたファイルを一時ファイルとして保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name
        logger.info(f"Temporarily saved uploaded file to {tmp_path}")

        # PptxLoaderを直接インスタンス化して使用
        loader = PptxLoader()
        # .load()メソッドはLoadPageContentsオブジェクトのリストを返す
        loaded_pages: List[LoadPageContents] = loader.load(path=tmp_path)

        # 各ページオブジェクトの.contents属性からテキストを取得
        if loaded_pages:
            for page in loaded_pages:
                texts.append(page.contents or "")

        logger.info(f"Extracted text from {len(texts)} pages.")

    except Exception as e:
        logger.error(f"Failed to parse PPTX file with PptxLoader: {e}", exc_info=True)
        raise
    finally:
        # 一時ファイルを削除
        if tmp_path and Path(tmp_path).exists():
            Path(tmp_path).unlink()

    return texts


# Contains AI-generated edits.
