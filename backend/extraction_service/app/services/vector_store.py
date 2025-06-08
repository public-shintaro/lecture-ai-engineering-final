import array
import base64
import logging
import os

import boto3
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


logger = logging.getLogger(__name__)

try:
    ddb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
    table = ddb.Table(os.getenv("DDB_TABLE", "SlideVectors"))
    logger.info(f"Successfully initialized DynamoDB client for table: {table.name}")
except Exception as e:
    logger.error(f"Failed to initialize DynamoDB client: {e}")
    table = None


def _to_b64(vec: list[float]) -> str:
    """Converts a list of floats to a base64 encoded string."""
    return base64.b64encode(array.array("f", vec).tobytes()).decode("utf-8")


def put_slide(pptx_id: str, slide_no: int, text: str, vec: list[float]):
    """Puts a single slide's data into the DynamoDB table."""
    if not table:
        raise ConnectionError("DynamoDB table is not initialized.")

    try:
        item = {
            "PK": f"pptx#{pptx_id}",
            "SK": f"slide#{slide_no:03}",
            "text": text,
            "vector_b64": _to_b64(vec),
        }
        table.put_item(Item=item)
        logger.info(f"Successfully put item to DynamoDB: {item['PK']} / {item['SK']}")
    except Exception as e:
        logger.error(f"Failed to put item to DynamoDB: {e}")
        raise HTTPException(status_code=500, detail=f"DynamoDB put_item failed: {e}")


# Contains AI-generated edits.
