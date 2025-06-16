import asyncio
import json
import logging
import os
import tempfile
from contextlib import asynccontextmanager

import aioboto3
from app.models import Chunk  # Chunkモデルをインポート

# 修正点: .servicesからではなく、 servicesから直接インポート
from app.services.embedding import generate_embedding
from app.services.parser import parse_pptx_to_texts
from app.services.vector_store import VectorStore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 環境変数
AWS_REGION = os.environ.get("AWS_REGION", "ap-northeast-1")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL")
UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]
EXTRACT_QUEUE_URL = os.environ["EXTRACT_QUEUE_URL"]
VECTOR_TABLE_NAME = os.environ["VECTOR_TABLE_NAME"]


@asynccontextmanager
async def create_boto_clients():
    session = aioboto3.Session(region_name=AWS_REGION)
    async with (
        session.client("sqs", endpoint_url=AWS_ENDPOINT_URL) as sqs,
        session.client("s3", endpoint_url=AWS_ENDPOINT_URL) as s3,
        session.resource("dynamodb", endpoint_url=AWS_ENDPOINT_URL) as dynamodb,
    ):
        yield sqs, s3, dynamodb


async def handle_message(msg: dict, s3_client, vector_store: VectorStore):
    receipt = msg["ReceiptHandle"]

    # ① Body をパース
    try:
        body = json.loads(msg["Body"])
        slide_id = body["slide_id"]
        s3_key = body["s3_key"]
    except (json.JSONDecodeError, KeyError):
        logging.warning("Unexpected message format, skipping: %s", msg["Body"])
        return receipt, True  # ⇒ Delete して終了

    # ② S3 → 一時ファイル DL
    with tempfile.NamedTemporaryFile() as tf:
        await s3_client.download_fileobj(UPLOAD_BUCKET, s3_key, tf)
        tf.seek(0)
        slide_texts = parse_pptx_to_texts(tf.read())  # bytes で渡す版に合わせる

    # ③ Chunk を作成 & 埋め込み & VectorStore に追加
    logging.info("Extracted %d chunks from %s", len(slide_texts), s3_key)
    for idx, text in enumerate(slide_texts):
        chunk = Chunk(
            slide_id=slide_id,
            chunk_id=f"{slide_id}-chunk-{idx:04d}",
            text=text,
            embedding=None,
            metadata={},
        )

        emb = generate_embedding(text)
        if emb is None:
            logging.warning("embedding failed: %s", chunk.chunk_id)
        else:
            chunk.embedding = emb
        await vector_store.add_chunk(chunk)  # ← add_chunk は既存メソッド

    logging.info("✔ upsert slide_id=%s chunks=%d", slide_id, len(slide_texts))
    return receipt, True  # 成功したので Delete


# --- ループ部の細かな修正だけ ---
async def main():
    logging.info("Starting SQS consumer…")
    async with create_boto_clients() as (sqs, s3, dynamodb):
        # aioboto3.resource/Table() は await 不要
        table = await dynamodb.Table(VECTOR_TABLE_NAME)
        vector_store = VectorStore(table)

        while True:
            resp = await sqs.receive_message(
                QueueUrl=EXTRACT_QUEUE_URL,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=20,
                VisibilityTimeout=120,
            )
            msgs = resp.get("Messages", [])
            if not msgs:
                continue

            results = await asyncio.gather(
                *[handle_message(m, s3, vector_store) for m in msgs]
            )

            for receipt, ok in results:
                if ok:
                    await sqs.delete_message(
                        QueueUrl=EXTRACT_QUEUE_URL, ReceiptHandle=receipt
                    )


# --------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
