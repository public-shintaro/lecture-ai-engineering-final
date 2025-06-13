import base64
import json
import logging
import os
from pathlib import Path

import boto3
import jinja2
from fastapi import HTTPException
from jinja2 import Environment
from models import VisionAnalysisResult

logger = logging.getLogger(__name__)

# --- (前半は変更なし) ---
BEDROCK_MODEL_ID = os.getenv("BEDROCK_VISION_MODEL_ID", "us.amazon.nova-lite-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# このファイル(/app/services/vision.py)の絶対パスを取得
current_file_path = Path(__file__).resolve()
# /app/services -> /app -> そこにあるtemplatesディレクトリを探す
templates_dir = current_file_path.parent.parent / "templates"

template_loader = jinja2.FileSystemLoader(searchpath=str(templates_dir))
env = Environment(loader=template_loader)
vision_template = env.get_template("vision_prompt.jinja")


def analyze_image_with_model(image_bytes: bytes) -> VisionAnalysisResult:
    """
    Analyzes an image using the specified Bedrock model and returns a structured response.
    """
    try:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        system_prompt = vision_template.render()

        # ユーザーが修正した、より正確なリクエストボディを使用
        request_body = {
            "schemaVersion": "messages-v1",
            "system": [{"text": system_prompt}],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "image": {
                                "format": "jpeg",
                                "source": {"bytes": image_base64},
                            }
                        },
                        {
                            "text": "Please analyze this slide image according to the system instructions."
                        },
                    ],
                }
            ],
        }

        # Bedrockモデルを呼び出し
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID, body=json.dumps(request_body)
        )

        # --- ▼▼▼ ここからが修正箇所 ▼▼▼ ---

        # 1. ストリームを読み込み、JSONとしてパース
        response_payload = json.loads(response.get("body").read())
        # (デバッグ用のprint文は不要なら削除してOKです)
        print("--- PARSED AI RESPONSE TEXT ---")
        print(response_payload)
        print("-----------------------------")

        # 2. 深い階層からAIの応答テキストを抽出
        raw_text = response_payload["output"]["message"]["content"][0]["text"]

        # 3. Markdownのコードブロック(` ```json ... ``` `)を削除
        #    最初の '{' と最後の '}' の間を抜き出すことで、確実なJSON文字列を取得
        json_start_index = raw_text.find("{")
        json_end_index = raw_text.rfind("}") + 1

        if json_start_index == -1 or json_end_index == 0:
            raise ValueError("No JSON object found in the model's response text.")

        json_string = raw_text[json_start_index:json_end_index]

        # 4. クリーンなJSON文字列をPythonの辞書に変換
        analysis_data = json.loads(json_string)
        # --- ▲▲▲ ここまでが修正箇所 ▲▲▲ ---

        # Pydanticモデルでバリデーションして返す
        return VisionAnalysisResult.model_validate(analysis_data)

    except json.JSONDecodeError as e:
        logger.error(
            f"Failed to parse JSON from model response: {analysis_data}", exc_info=True
        )
        raise HTTPException(
            status_code=502, detail=f"Invalid JSON format from AI service: {e}"
        )
    except Exception as e:
        logger.error(
            f"Bedrock API call failed for {BEDROCK_MODEL_ID}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=502, detail=f"Error communicating with AI service: {e}"
        )


# Contains AI-generated edits.
