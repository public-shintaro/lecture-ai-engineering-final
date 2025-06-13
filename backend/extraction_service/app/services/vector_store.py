import logging
import os
from decimal import Decimal
from typing import TYPE_CHECKING, List

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# ▼▼▼ TYPE_CHECKINGブロックを追加 ▼▼▼
# 型ヒントのためだけにインポートし、実行時にはインポートしないようにする
if TYPE_CHECKING:
    from models import Chunk

logger = logging.getLogger(__name__)


class VectorStore:
    """
    DynamoDBと連携し、ベクトルデータの永続化を管理するクラス。
    """

    def __init__(self, table_name: str | None = None, region_name: str | None = None):
        # ... (この部分のコードは変更なし) ...
        try:
            self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
            self.table_name = table_name or os.environ.get(
                "DDB_TABLE_NAME", "SlideChunks"
            )
            if not self.table_name:
                raise ValueError("DynamoDB table name is not configured.")
            dynamodb = boto3.resource("dynamodb", region_name=self.region_name)
            self.table = dynamodb.Table(self.table_name)
            self.table.load()
            logger.info(
                f"Successfully connected to DynamoDB table: '{self.table_name}'"
            )
        except ClientError as e:
            logger.exception(
                f"Failed to connect to DynamoDB table '{self.table_name}': {e}"
            )
            raise

    # ▼▼▼ 型ヒントを文字列（Forward Reference）に変更 ▼▼▼
    def add_chunk(self, chunk: "Chunk"):
        """
        単一のChunkオブジェクトをDynamoDBテーブルに追加する。
        """
        try:
            item = chunk.model_dump()
            # embeddingのリストが存在する場合、中のfloatをすべてDecimalに変換する
            if item.get("embedding"):
                item["embedding"] = [Decimal(str(x)) for x in item["embedding"]]
            self.table.put_item(Item=item)
            logger.info(
                f"Successfully put chunk to DynamoDB: {chunk.document_id} / {chunk.chunk_id}"
            )
        except ClientError as e:
            logger.exception(f"Failed to put chunk {chunk.chunk_id} to DynamoDB: {e}")
            raise

    # ▼▼▼ 型ヒントを文字列（Forward Reference）に変更し、メソッド内でインポート ▼▼▼
    def get_chunks_by_document_id(self, document_id: str) -> List["Chunk"]:
        """
        指定されたdocument_idに一致するすべてのチャンクをDynamoDBから取得する。
        """
        # ▼▼▼ 実際に必要になったここでインポートする！ ▼▼▼
        from models import Chunk  # noqa: E402

        try:
            response = self.table.query(
                KeyConditionExpression=Key("document_id").eq(document_id)
            )
            items = response.get("Items", [])
            return [Chunk(**item) for item in items]
        except ClientError as e:
            logger.exception(
                f"Failed to query chunks for document_id {document_id}: {e}"
            )
            raise
