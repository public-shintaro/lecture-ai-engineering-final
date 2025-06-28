# app.py  ―  Streamlit Fronend (最小 MVP)
import os
import uuid
from typing import Any, Dict, cast

import requests
import streamlit as st

UPLOAD_API = os.getenv("UPLOAD_API_URL", "http://upload_service:8000/api/v1/upload")
FACT_API = os.getenv("FACTCHECK_API_URL", "http://upload_service:8000/api/v1/factcheck")

st.set_page_config(page_title="Slide FactChecker", page_icon="🧐")

st.title("🧐 Lecture-Slide Fact Checker (Streamlit MVP)")

###############################################################################
# 1. pptx アップロード
###############################################################################
st.header("1️⃣ Upload PPTX")
pptx_file = st.file_uploader("PowerPoint (.pptx) を選択してください", type=["pptx"])

if pptx_file is not None:
    slide_id = uuid.uuid4().hex  # BE 要求
    if st.button("🚀 Upload"):
        with st.spinner("アップロード中 …"):
            files = {
                "file": (
                    pptx_file.name,
                    pptx_file,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            }
            data = {"slide_id": slide_id}
            resp = requests.post(UPLOAD_API, files=files, data=data, timeout=300)
            resp.raise_for_status()
        st.success(f"✅ Upload 完了！ slide_id = {slide_id}")
        st.session_state["slide_id"] = slide_id  # 後続で使用

###############################################################################
# 2. Fact-check 実行
###############################################################################
st.header("2️⃣ Fact-Check")
sid = st.session_state.get("slide_id")
if sid:
    page_input = st.text_input(
        "確認したいページ番号（例: 1,3,5）。空欄=全ページ", key="pages"
    )
    if st.button("🔍 Fact-check 実行"):
        payload = {"slide_id": sid}
        if page_input.strip():
            # 数字 or カンマ区切り → int list
            pages = [int(p) for p in page_input.split(",") if p.strip().isdigit()]
            payload["pages"] = pages
        with st.spinner("Bedrock で Fact-check 中 …（少しかかります）"):
            res = requests.post(FACT_API, json=payload, timeout=600)
            res.raise_for_status()
            data2: Dict[str, Any] = cast(Dict[str, Any], res.json())

        # -----------------------------------------------------------
        # 結果表示
        # -----------------------------------------------------------
        st.subheader("📄 ページ別結果")
        for page in data2["per_page_results"]:
            with st.expander(f"Page {page['page']}"):
                st.json(page)

        if "slide_summary" in data2:
            st.subheader("📝 スライド全体サマリー")
            st.json(data2["slide_summary"])
else:
    st.info("まず PPTX をアップロードしてください。")

###############################################################################
st.markdown("---\n© 2025 AIE2504 Demo")
