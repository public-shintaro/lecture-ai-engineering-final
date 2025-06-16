# backend/extraction_service/app/services/factcheck.py

import json
import logging
import os
from pathlib import Path  # <- pathlibをインポート

import boto3
import jinja2
from app.dependencies import get_vector_store
from app.models import Inconsistency
from sklearn.metrics.pairwise import cosine_similarity

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 定数設定
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = "us.amazon.nova-lite-v1:0"  # ② モデルIDを修正
TOP_K_EVIDENCE = 5

# pathlibを使って、このファイル自身の絶対パスを取得
try:
    current_file_path = Path(__file__).resolve()
    templates_dir = current_file_path.parent.parent.parent / "templates"
    template_loader = jinja2.FileSystemLoader(searchpath=str(templates_dir))
    env = jinja2.Environment(loader=template_loader)
    PROMPT_TEMPLATE = env.get_template("factcheck_prompt.jinja")
except Exception as e:
    logger.critical(f"Failed to load Jinja2 template: {e}", exc_info=True)
    PROMPT_TEMPLATE = None

# AWSクライアントとサービスを初期化
bedrock_runtime = None
vector_store = None
try:
    if PROMPT_TEMPLATE:
        bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        vector_store = get_vector_store()
except Exception as e:
    logger.critical(
        f"Failed to initialize AWS clients or VectorStore: {e}", exc_info=True
    )


def _get_factcheck_from_llm(claim: str, evidence: str) -> dict | None:
    """Bedrockモデルを呼び出し、ファクトチェック判定を取得する。"""
    if not bedrock_runtime or not PROMPT_TEMPLATE:
        logger.error("Bedrock runtime or prompt template is not available.")
        return None

    system_prompt = PROMPT_TEMPLATE.render(claim=claim, evidence=evidence)

    try:
        # ▼▼▼【修正点3】Bedrock呼び出しをお手本に合わせる ▼▼▼
        # Nova Liteが期待するMessages APIの形式でリクエストボディを作成
        request_body = {
            "schemaVersion": "messages-v1",
            "system": [{"text": system_prompt}],
            "messages": [{"role": "user", "content": [{"text": system_prompt}]}],
        }
        body = json.dumps(request_body)

        response = bedrock_runtime.invoke_model(body=body, modelId=BEDROCK_MODEL_ID)
        # 1. ストリームを読み込み、JSONとしてパース
        response_payload = json.loads(response.get("body").read())

        # 2. ご提示のスキーマに従い、深い階層からAIの応答テキストを抽出
        #    vision.pyのお手本と同じロジック
        try:
            raw_text = response_payload["output"]["message"]["content"][0]["text"]
        except (KeyError, IndexError) as e:
            logger.error(
                f"Could not extract text from Bedrock response. Structure may be unexpected. Error: {e}. Response: {response_payload}"
            )
            raise ValueError("Could not extract text from Bedrock response.")

        # 3. Markdownのコードブロックなどを削除し、確実なJSON文字列を取得
        json_start_index = raw_text.find("{")
        json_end_index = raw_text.rfind("}") + 1

        if json_start_index == -1 or json_end_index == 0:
            logger.error(
                f"No JSON object found in the model's response text. Response: {raw_text}"
            )
            raise ValueError("No JSON object found in the model's response text.")

        json_string = raw_text[json_start_index:json_end_index]

        # 4. クリーンなJSON文字列をPythonの辞書に変換
        analysis_data = json.loads(json_string)

        return analysis_data

    except Exception as e:
        logger.exception(
            f"Error calling Bedrock model for claim '{claim[:50]}...': {e}"
        )
        return None


# `factcheck_slide`関数自体は、呼び出すヘルパー関数が変わる以外は大きな変更なし
def factcheck_slide(slide_id: str) -> list[Inconsistency]:
    """指定されたスライドIDのすべてのチャンクに対してファクトチェックを実行する。"""
    if not vector_store:
        logger.error("VectorStore is not initialized. Cannot perform fact-check.")
        return []

    logger.info(f"Starting fact-check for slide_id: {slide_id}")
    inconsistencies = []

    try:
        # ③ 追加された関数を呼び出す
        all_chunks = vector_store.get_chunks_by_document_id(slide_id)
        if not all_chunks or len(all_chunks) < 2:
            logger.warning(
                f"Not enough chunks ({len(all_chunks)}) found for slide_id {slide_id} to perform fact-check."
            )
            return []
    except Exception:
        logger.exception(
            f"Failed to retrieve chunks for slide_id {slide_id} from vector store."
        )
        return []

    for claim_chunk in all_chunks:
        if not claim_chunk.embedding:
            logger.warning(
                f"Skipping chunk {claim_chunk.chunk_id} due to missing embedding."
            )
            continue

        evidence_candidate_chunks = [
            c for c in all_chunks if c.chunk_id != claim_chunk.chunk_id and c.embedding
        ]
        if not evidence_candidate_chunks:
            continue

        evidence_embeddings = [c.embedding for c in evidence_candidate_chunks]
        similarities = cosine_similarity([claim_chunk.embedding], evidence_embeddings)[
            0
        ]

        top_k_indices = similarities.argsort()[-TOP_K_EVIDENCE:][::-1]
        top_evidence_chunks = [evidence_candidate_chunks[i] for i in top_k_indices]
        evidence_text = "\n---\n".join([c.text for c in top_evidence_chunks])

        llm_result = _get_factcheck_from_llm(
            claim=claim_chunk.text, evidence=evidence_text
        )

        if llm_result:
            verdict = llm_result.get("verdict")
            score = llm_result.get("score")
            reason = llm_result.get("reason")

            if (
                verdict
                and score is not None
                and (verdict == "contradiction" or score < 0.5)
            ):
                if verdict not in ["supported", "contradiction", "not_enough_info"]:
                    logger.warning(
                        f"LLM returned an invalid verdict: '{verdict}'. Skipping."
                    )
                    continue

                inconsistency = Inconsistency(
                    slide_id=slide_id,
                    chunk_id=claim_chunk.chunk_id,
                    claim=claim_chunk.text,
                    evidence=evidence_text,
                    verdict=verdict,
                    score=score,
                )
                inconsistencies.append(inconsistency)
                logger.info(
                    f"Found inconsistency for chunk {claim_chunk.chunk_id}: verdict={verdict}, score={score}, reason={reason}"
                )

    logger.info(
        f"Finished fact-check for slide_id: {slide_id}. Found {len(inconsistencies)} inconsistencies."
    )
    return inconsistencies
