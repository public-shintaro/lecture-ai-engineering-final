import logging
import tempfile
from pathlib import Path
from typing import List

# 高レベルな関数ではなく、PptxLoaderを直接インポートします
from exparso.loader.pptx_loader import PptxLoader

# PptxLoaderが返すオブジェクトの型もインポートします
from exparso.model import LoadPageContents

logger = logging.getLogger(__name__)


def parse_pptx_to_texts(file_content: bytes) -> List[str]:
    """
    exparso.PptxLoaderを直接使用して、PPTXファイルのバイトデータから各スライドのテキストを抽出する。
    """
    texts: List[str] = []
    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            # ▼▼▼ file.file.read() を file_content に変更 ▼▼▼
            tmp.write(file_content)
            tmp_path = tmp.name
        logger.info(f"Temporarily saved uploaded file to {tmp_path}")

        loader = PptxLoader()
        loaded_pages: List[LoadPageContents] = loader.load(path=tmp_path)

        if loaded_pages:
            for page in loaded_pages:
                texts.append(page.contents or "")
        logger.info(f"Extracted text from {len(texts)} pages.")

    except Exception as e:
        logger.error(f"Failed to parse PPTX file with PptxLoader: {e}", exc_info=True)
        raise
    finally:
        if tmp_path and Path(tmp_path).exists():
            Path(tmp_path).unlink()

    return texts


# Contains AI-generated edits.
