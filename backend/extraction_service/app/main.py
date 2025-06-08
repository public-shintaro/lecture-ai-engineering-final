import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

# servicesモジュールを絶対パスでインポート
from app.services import embedding, parser, vector_store

# 全てのインポート処理が始まる前に、.envファイルの内容を環境変数に読み込む
load_dotenv()
print("--- DEBUGGING ENVIRONMENT VARIABLES ---")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
session_token = os.getenv("AWS_SESSION_TOKEN")
print(f"AWS_ACCESS_KEY_ID: {access_key}")
# シークレットキーそのものは表示せず、存在有無だけ確認
print(f"AWS_SECRET_ACCESS_KEY: {'[SET]' if secret_key else '[NOT SET]'}")
# セッショントークンは空文字かどうかが重要なのでクォートで囲って表示
print(f"AWS_SESSION_TOKEN: '{session_token}'")
print("--- END DEBUGGING ---")
# --- ↑↑↑ ここまで追加 ↑↑↑ ---


# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Extraction and Embedding Service",
    description="Extracts content from presentation files, generates embeddings, and indexes them into DynamoDB.",
    version="0.3.0",
)


@app.get("/health", summary="Health Check")
def health_check():
    """
    Simple health check endpoint to confirm the service is running.
    """
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}


@app.post("/embed", summary="Extract, Embed, and Index PPTX to DynamoDB")
async def embed_document(file: UploadFile = File(...)):
    """
    Receives a PPTX file and performs the following steps:
    1.  Extracts text content from each slide.
    2.  Generates vector embeddings for each slide's text.
    3.  Indexes the text and vectors into DynamoDB.
    """
    if not file.filename.endswith(".pptx"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .pptx is supported."
        )

    try:
        logger.info(f"Starting embedding process for file: {file.filename}")

        slide_texts = parser.extract_text_from_pptx(file)
        if not slide_texts:
            raise HTTPException(status_code=400, detail="Could not extract any text.")

        slide_vectors = embedding.get_embeddings(slide_texts)

        for idx, (text, vec) in enumerate(zip(slide_texts, slide_vectors), start=1):
            if text and vec:
                vector_store.put_slide(
                    pptx_id=file.filename, slide_no=idx, text=text, vec=vec
                )

        logger.info(f"Successfully processed and indexed {file.filename}")
        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "message": "File successfully extracted, embedded, and indexed into DynamoDB.",
                "slides_processed": len(slide_texts),
            },
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during embedding for {file.filename}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail=f"An internal error occurred: {str(e)}"
        )


# Contains AI-generated edits.
