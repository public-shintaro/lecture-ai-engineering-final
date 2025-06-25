import logging
from decimal import Decimal
from typing import TYPE_CHECKING, List

# boto3.dynamodb.conditions は非同期でも共通で利用可能
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# 型ヒントのためだけにインポート
if TYPE_CHECKING:
    from app.models import Chunk

logger = logging.getLogger(__name__)


class VectorStore:
    """
    DynamoDBと非同期に連携し、ベクトルデータの永続化を管理するクラス。
    """

    def __init__(self, table):
        """
        コンストラクタ。boto3リソースを直接作成するのではなく、
        外部から非同期のaioboto3テーブルリソースを受け取るように変更。

        Args:
            table: aioboto3で初期化されたDynamoDB.Tableリソース
        """
        if table is None:
            raise ValueError("aioboto3 DynamoDB.Table resource cannot be None.")
        self.table = table
        logger.info(f"VectorStore initialized with table: '{self.table.name}'")

    def add_chunk(self, chunk: "Chunk"):
        """
        単一のChunkオブジェクトをDynamoDBテーブルに非同期で追加する。
        """
        try:
            # Pydanticモデルを辞書に変換
            item = chunk.model_dump()

            # embeddingのリストが存在する場合、中のfloatをすべてDecimalに変換する
            # DynamoDBはfloatを直接サポートしないため、この変換は必須
            if item.get("embedding"):
                item["embedding"] = [Decimal(str(x)) for x in item["embedding"]]

            # テーブルへの書き込みを非同期で実行
            self.table.put_item(Item=item)

            logger.debug(
                f"Successfully put chunk to DynamoDB: {chunk.slide_id} / {chunk.chunk_id}"
            )
        except ClientError as e:
            logger.exception(f"Failed to put chunk {chunk.chunk_id} to DynamoDB: {e}")
            raise

    async def get_chunks_by_document_id(self, document_id: str) -> List["Chunk"]:
        """
        指定されたdocument_idに一致するすべてのチャンクを非同期でDynamoDBから取得する。
        """
        from app.models import Chunk

        try:
            # テーブルへのクエリを非同期で実行
            response = await self.table.query(
                KeyConditionExpression=Key("document_id").eq(document_id)
            )
            items = response.get("Items", [])

            # DynamoDBから取得したDecimalをfloatに戻してからモデルを初期化する
            for item in items:
                if "embedding" in item and item["embedding"] is not None:
                    item["embedding"] = [float(x) for x in item["embedding"]]

            return [Chunk(**item) for item in items]
        except ClientError as e:
            logger.exception(
                f"Failed to query chunks for document_id {document_id}: {e}"
            )
            raise
