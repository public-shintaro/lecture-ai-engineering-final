import os
import time
import uuid
from pathlib import Path

import pytest
import requests

# ---------------- Service endpoints ----------------
UPLOAD_API_URL = os.getenv(
    "UPLOAD_API_URL",
    "http://upload_service:8000/api/v1/upload",
)
FACTCHECK_API_URL = os.getenv(
    "FACTCHECK_API_URL",
    "http://upload_service:8000/api/v1/factcheck",  # 同じ BE にマウントしていればこれで OK
)

# ---------------- Config ---------------------------
SAMPLE_PPTX = Path(__file__).parent / "test_sample.pptx"
WAIT_SECS_AFTER_UPLOAD = int(os.getenv("WAIT_AFTER_UPLOAD", "30"))  # embed 完了待ち
RETRY_FACTCHECK = 3  # 404(まだチャンク無い) 時のリトライ回数
RETRY_INTERVAL = 10  # 秒


@pytest.mark.integration
def test_factcheck_api_real_bedrock():
    """
    1. PPTX をアップロードしてチャンクを生成
    2. embed が DynamoDB に書き込まれるまで待機
    3. /api/v1/factcheck を叩き、正常 JSON が返ることを確認
    """
    assert SAMPLE_PPTX.exists(), "tests/test_sample.pptx が見つかりません"

    slide_id = uuid.uuid4().hex
    with SAMPLE_PPTX.open("rb") as f:
        files = {
            "file": (
                SAMPLE_PPTX.name,
                f,
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        }
        data = {"slide_id": slide_id}
        up = requests.post(UPLOAD_API_URL, files=files, data=data, timeout=60)
    up.raise_for_status()
    assert up.json()["slide_id"] == slide_id
    chunks = up.json().get("chunks", 0)
    assert chunks > 0, "チャンク数が 0 です"

    # -------- embed → DynamoDB 反映待ち -------------
    time.sleep(WAIT_SECS_AFTER_UPLOAD)

    # -------- FactCheck API 呼び出し (リトライ付き) ---
    last_err = None
    for _ in range(RETRY_FACTCHECK):
        try:
            fc = requests.post(
                FACTCHECK_API_URL, json={"slide_id": slide_id}, timeout=120
            )
            if fc.status_code == 404:
                # まだチャンクが見つからない場合は再試行
                time.sleep(RETRY_INTERVAL)
                continue
            fc.raise_for_status()
            break
        except requests.RequestException as e:
            last_err = e
            time.sleep(RETRY_INTERVAL)
    else:
        pytest.fail(f"FactCheck API failed after retries: {last_err}")

    data = fc.json()

    # ------------- 最低限の構造チェック --------------
    assert (
        "per_page_results" in data and data["per_page_results"]
    ), "per_page_results が空"
    first = data["per_page_results"][0]
    assert {"page", "issues"}.issubset(first), "per-page フィールドが不足"

    # pages を省略しているため slide_summary も期待
    assert "slide_summary" in data, "slide_summary がありません"
    for summary in data["slide_summary"].values():
        print(summary)
    # ------------- ざっくり内容をプリント -----------
    print(
        "\n✅ FactCheck OK:",
        f"pages={len(data['per_page_results'])},",
        f"summary_keys={list(data['slide_summary'].keys())}",
    )
