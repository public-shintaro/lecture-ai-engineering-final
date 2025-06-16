import logging
import os
from typing import TYPE_CHECKING

import boto3
from botocore.exceptions import ClientError

# 修正点: 絶対パスでVectorStoreをインポートする
from backend.extraction_service.app.services.vector_store import VectorStore

if TYPE_CHECKING:
    from backend.extraction_service.app.services.vector_store import VectorStore

logger = logging.getLogger(__name__)

# この後の初期化ロジックは変更なし
vector_store: "VectorStore | None" = None
try:
    table_name = os.environ.get("VECTOR_TABLE_NAME", "lecture-vector-store-dev")

    sync_dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "ap-northeast-1"),
        endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
    )
    sync_table = sync_dynamodb.Table(table_name)

    vector_store = VectorStore(table=sync_table)

    logger.info("Successfully initialized VectorStore for FastAPI.")

except (ClientError, ImportError, ValueError) as e:
    # 循環参照エラーを防ぐため、エラーログの出力場所を修正
    logging.error(f"Could not initialize VectorStore for FastAPI: {e}", exc_info=True)
    vector_store = None


def get_vector_store() -> "VectorStore":
    if vector_store is None:
        raise RuntimeError("VectorStore is not available.")
    return vector_store
