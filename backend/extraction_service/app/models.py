from typing import List

from pydantic import BaseModel, Field


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


class SuggestedSourceResult(BaseModel):
    """Represents a suggested source for further reading or evidence."""

    title: str = Field(description="The title of the suggested source.")
    url: str = Field(description="A direct URL to the suggested source.")


class VisionAnalysisResult(BaseModel):
    """The structured JSON response from the vision analysis service."""

    fact_check: FactCheckResult
    suggested_sources: List[SuggestedSourceResult]


# Contains AI-generated edits.
