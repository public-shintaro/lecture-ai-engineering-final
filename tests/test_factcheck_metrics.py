# tests/test_factcheck_metrics.py

import json
import os
from pathlib import Path

import pytest
import requests  # FastAPIサーバーへのHTTPリクエストにのみ依存

# --- 定数設定 ---
GROUND_TRUTH_DIR = Path(__file__).parent.parent / "data" / "ground_truth"
# テスト対象のFastAPIサーバーのURL
API_BASE_URL = os.getenv("UPLOAD_API_URL", "http://upload_service:8000")
# /embedで取得したテストしたいdocument_id
# 実際のテスト実行時には、ご自身のIDに書き換えてください
TEST_DOCUMENT_ID = "86e3e0d8-2d58-473c-ba00-a4249b7fd222"
# 性能要件で定義した適合率の閾値
PRECISION_THRESHOLD = 0.8


def load_ground_truth(doc_id: str) -> set[str]:
    """
    正解ファイル（JSON）を読み込み、「矛盾している」と定義されたchunk_idのセットを返す。
    """
    gt_path = GROUND_TRUTH_DIR / f"{doc_id}.json"
    if not gt_path.exists():
        pytest.fail(f"Ground truth file not found at: {gt_path}")

    with open(gt_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return {
            item["chunk_id"]
            for item in data
            if item.get("expected_verdict") == "contradiction"
        }


def get_predictions_from_api(doc_id: str) -> set[str]:
    """
    FastAPIの/factcheckエンドポイントを呼び出し、
    「矛盾している」と予測されたchunk_idのセットを返す。
    """
    url = f"{API_BASE_URL}/api/v1/factcheck"
    try:
        response = requests.post(url, json={"slide_id": doc_id}, timeout=300)
        response.raise_for_status()

        predicted_inconsistencies = response.json()
        return {
            item["chunk_id"]
            for item in predicted_inconsistencies
            if item.get("verdict") == "contradiction"
        }
    except requests.RequestException as e:
        pytest.fail(f"API call to {url} failed: {e}")
        return set()


# @pytest.mark.xfail(reason="初期実装ではまだ性能目標に到達していない可能性があるため")
def test_factcheck_precision_via_api():
    """
    【ブラックボックステスト】
    FastAPIエンドポイント経由でファクトチェック機能の適合率を評価する。
    """
    # 1. 正解データを読み込む
    true_contradictory_chunks = load_ground_truth(TEST_DOCUMENT_ID)

    # 2. APIを呼び出して予測結果を取得
    predicted_contradictory_chunks = get_predictions_from_api(TEST_DOCUMENT_ID)

    # 3. 適合率(Precision)を計算
    #    TP = 予測と正解の両方に存在するchunkの数
    #    FP = 予測には存在するが、正解には存在しないchunkの数
    #    Precision = TP / (TP + FP)

    true_positives = len(
        predicted_contradictory_chunks.intersection(true_contradictory_chunks)
    )
    predicted_positives = len(predicted_contradictory_chunks)

    if predicted_positives == 0:
        # 何も予測しなかった場合、適合率は1.0とするか、テストをスキップするかを選択
        # ここでは、矛盾がないと正しく予測したとみなし、1.0とする
        precision = 1.0
    else:
        precision = true_positives / predicted_positives

    print(f"\n--- Black-Box Test Results for document: {TEST_DOCUMENT_ID} ---")
    print(f"True contradictions (Ground Truth): {len(true_contradictory_chunks)}")
    print(f"Predicted contradictions (API):   {len(predicted_contradictory_chunks)}")
    print(f"Correctly Predicted (TP):         {true_positives}")
    print("--------------------------------------------------")
    print(f"Calculated Precision: {precision:.4f}")
    print(f"Required Threshold:   {PRECISION_THRESHOLD:.4f}")

    # 4. アサーション: 適合率が閾値以上であることを確認
    assert precision >= PRECISION_THRESHOLD, (
        f"適合率が閾値({PRECISION_THRESHOLD})を下回りました: {precision:.4f}"
    )
