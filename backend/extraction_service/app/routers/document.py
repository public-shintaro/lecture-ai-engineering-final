import logging
import uuid

# main.pyで初期化されたvector_storeインスタンスをインポートして利用
from app.dependencies import vector_store

# Chunkモデルをインポート
from app.models import Chunk
from app.services import embedding, parser
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/document", tags=["Document Processing"])


def process_and_store_document(file_content: bytes, document_id: str, filename: str):
    """
    バックグラウンドでファイルの解析、Chunk化、ベクトル化、保存を行う。
    """
    try:
        logger.info(f"[BackgroundTask] Started processing for doc_id: {document_id}")

        # 1. parser.pyを呼び出して、スライドごとのテキストリストを取得
        slide_texts = parser.parse_pptx_to_texts(file_content)

        if not slide_texts:
            logger.warning(f"Could not extract any text from file: {filename}")
            return

        # 2. テキストリストをループし、Chunkオブジェクトに変換・処理する
        for i, text in enumerate(slide_texts):
            # チャンクIDを生成
            chunk_id = f"{document_id}-chunk-{i:04d}"

            # Chunkオブジェクトを作成
            chunk = Chunk(
                document_id=document_id,
                chunk_id=chunk_id,
                text=text,
                metadata={},  # メタデータは空で初期化
                embedding=None,
            )

            # 3. 各チャンクをベクトル化
            if chunk.text:
                chunk.embedding = embedding.generate_embedding(chunk.text)

            # 4. 各チャンクをDBに保存
            if vector_store:
                vector_store.add_chunk(chunk)

        logger.info(
            f"[BackgroundTask] Successfully finished processing and storing {len(slide_texts)} chunks for doc_id: {document_id}"
        )

    except Exception as e:
        logger.error(
            f"[BackgroundTask] Failed processing for doc_id {document_id}: {e}",
            exc_info=True,
        )


@router.post("/embed", summary="Accept and process a PPTX file", status_code=202)
async def embed_document(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    if not file.filename.endswith(".pptx"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .pptx is supported."
        )
    if not vector_store:
        raise HTTPException(
            status_code=503,
            detail="Service Unavailable: Vector store is not connected.",
        )

    document_id = str(uuid.uuid4())
    file_content = await file.read()
    background_tasks.add_task(
        process_and_store_document, file_content, document_id, file.filename
    )

    logger.info(
        f"Accepted file '{file.filename}'. Processing started with doc_id: {document_id}"
    )
    return {
        "message": "File accepted. Processing started in the background.",
        "document_id": document_id,
    }
