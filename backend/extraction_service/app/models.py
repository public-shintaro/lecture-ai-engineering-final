from typing import List, Literal

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    metadata: dict
    embedding: list[float] | None = None


class FactCheckResult(BaseModel):
    """Represents the result of a fact-check analysis."""

    issues: List[str] = Field(
        description="A list of potential factual inaccuracies or claims requiring citation."
    )
    confidence: float = Field(
        description="A score from 0.0 to 1.0 indicating confidence in the identified issues.",
        ge=0.0,
        le=1.0,
    )


class Inconsistency(BaseModel):
    """
    ファクトチェックによって検出された「不整合」情報を格納するスキーマ。
    """

    slide_id: str = Field(..., description="不整合が検出されたスライドのID")
    chunk_id: str = Field(..., description="不整合が検出されたテキストチャンクのID")
    claim: str = Field(..., description="検証対象となった主張・記述")
    evidence: str | None = Field(
        None, description="主張を検証するために使用された根拠となる情報"
    )
    verdict: Literal["supported", "contradiction", "not_enough_info"] = Field(
        ...,
        description="LLMによる判定結果 (supported: 支持, contradiction: 矛盾, not_enough_info: 情報不足)",
    )
    score: float = Field(
        ..., ge=0.0, le=1.0, description="判定の信頼度スコア (0.0から1.0の範囲)"
    )


class SuggestedSourceResult(BaseModel):
    """Represents a suggested source for further reading or evidence."""

    title: str = Field(description="The title of the suggested source.")
    url: str = Field(description="A direct URL to the suggested source.")


class VisionAnalysisResult(BaseModel):
    """The structured JSON response from the vision analysis service."""

    fact_check: FactCheckResult
    suggested_sources: List[SuggestedSourceResult]


# Contains AI-generated edits.
