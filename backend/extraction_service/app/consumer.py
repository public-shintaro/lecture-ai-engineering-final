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
from botocore.exceptions import ClientError

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


async def handle_message(message: dict, s3_client, vector_store: VectorStore):
    receipt_handle = message["ReceiptHandle"]
    try:
        # 修正点: S3イベント通知のJSONを正しくパースする
        logging.info(f"Received message body: {message['Body']}")
        body = json.loads(message["Body"])
        # S3イベント通知ではない、予期せぬメッセージはスキップ
        if "Records" not in body:
            logging.warning("Message is not a valid S3 event notification, skipping.")
            return receipt_handle, True  # 処理対象外なのでキューから削除

        s3_key = body["Records"][0]["s3"]["object"]["key"]
        logging.info(f"Processing S3 object: {s3_key}")

        with tempfile.NamedTemporaryFile() as tf:
            await s3_client.download_fileobj(UPLOAD_BUCKET, s3_key, tf)
            tf.seek(0)

            # チャンク化の際にslide_idとしてファイル名（拡張子なし）を使用
            slide_id = os.path.splitext(os.path.basename(s3_key))[0]
            slide_texts = parse_pptx_to_texts(tf.name)  # parser関数を修正

            chunks = []
            for i, text in enumerate(slide_texts):
                chunk_id = f"{slide_id}-chunk-{i:04d}"
                chunks.append(
                    Chunk(
                        slide_id=slide_id,
                        chunk_id=chunk_id,
                        text=text,
                        page_number=i + 1,
                        embedding=None,
                    )
                )

        logging.info(f"Extracted {len(chunks)} chunks from {s3_key}")

        for chunk in chunks:
            embedding = generate_embedding(chunk.text)
            if embedding is None:
                logging.warning(
                    f"Failed to generate embedding for chunk: {chunk.chunk_id}. Skipping."
                )
                continue

            chunk.embedding = embedding
            await vector_store.add_chunk(chunk)

        logging.info(f"Successfully processed and stored all chunks for {s3_key}")
        return receipt_handle, True

    except json.JSONDecodeError:
        logging.warning(
            f"Received a non-JSON message, deleting from queue: {message['Body']}"
        )
        return receipt_handle, True  # JSONでないメッセージは処理できないので削除
    except Exception as e:
        logging.error(f"Failed to process message. Error: {e}", exc_info=True)
        return receipt_handle, False


async def main():
    logging.info("Starting SQS consumer...")
    async with create_boto_clients() as (sqs, s3, dynamodb):
        table = await dynamodb.Table(VECTOR_TABLE_NAME)
        vector_store = VectorStore(table)

        while True:
            try:
                response = await sqs.receive_message(
                    QueueUrl=EXTRACT_QUEUE_URL,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=20,
                    VisibilityTimeout=120,
                )
                messages = response.get("Messages", [])
                if not messages:
                    continue

                tasks = [handle_message(msg, s3, vector_store) for msg in messages]
                results = await asyncio.gather(*tasks)

                for receipt_handle, success in results:
                    if success:
                        await sqs.delete_message(
                            QueueUrl=EXTRACT_QUEUE_URL, ReceiptHandle=receipt_handle
                        )

            except ClientError as e:
                logging.error(f"SQS client error: {e}")
                await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
