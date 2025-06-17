# tests/schema_factcheck.py

import pytest
from pydantic import ValidationError

# インポート元を修正
from backend.extraction_service.app.models import Inconsistency


def test_inconsistency_schema_valid():
    """正常なデータでInconsistencyモデルが正しくパースできることをテストする"""
    valid_data = {
        "slide_id": "slide-001",
        "chunk_id": "chunk-003",
        "claim": "AIの市場規模は2030年に1兆ドルに達する。",
        "evidence": "世界経済フォーラムのレポートでは1.5兆ドルと予測。",
        "verdict": "contradiction",
        "score": 0.25,
    }
    inconsistency = Inconsistency.model_validate(valid_data)
    assert inconsistency.slide_id == "slide-001"
    assert inconsistency.verdict == "contradiction"
    assert inconsistency.score == 0.25


# ... (他のテスト関数は変更なし) ...


def test_inconsistency_schema_evidence_none():
    """evidenceがNoneの場合でも正しくパースできることをテストする"""
    no_evidence_data = {
        "slide_id": "slide-002",
        "chunk_id": "chunk-015",
        "claim": "2050年の火星旅行に関する言及",
        "evidence": None,
        "verdict": "not_enough_info",
        "score": 0.5,
    }
    inconsistency = Inconsistency.model_validate(no_evidence_data)
    assert inconsistency.evidence is None
    assert inconsistency.verdict == "not_enough_info"


def test_inconsistency_schema_invalid_verdict():
    """不正なverdictを持つデータでValidationErrorが発生することをテストする"""
    invalid_data = {
        "slide_id": "slide-001",
        "chunk_id": "chunk-004",
        "claim": "テストクレーム",
        "evidence": "テストエビデンス",
        "verdict": "maybe",  # 不正な値
        "score": 0.9,
    }
    with pytest.raises(ValidationError):
        Inconsistency.model_validate(invalid_data)


def test_inconsistency_schema_score_out_of_range():
    """スコアが0-1の範囲外の場合にValidationErrorが発生することをテストする"""
    out_of_range_data = {
        "slide_id": "slide-001",
        "chunk_id": "chunk-005",
        "claim": "テストクレーム",
        "evidence": "テストエビデンス",
        "verdict": "supported",
        "score": 1.5,  # 範囲外
    }
    with pytest.raises(ValidationError):
        Inconsistency.model_validate(out_of_range_data)


def test_inconsistency_schema_missing_field():
    """必須フィールド(claim)が欠落しているデータでValidationErrorが発生することをテストする"""
    missing_field_data = {
        "slide_id": "slide-001",
        "chunk_id": "chunk-006",
        # "claim" フィールドが欠落
        "evidence": "テストエビデンス",
        "verdict": "supported",
        "score": 0.9,
    }
    with pytest.raises(ValidationError):
        Inconsistency.model_validate(missing_field_data)
