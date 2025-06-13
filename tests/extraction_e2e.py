import os
from pathlib import Path

import pytest
import requests  # E2Eテスト用にrequestsを追加する必要があります (requirements-dev.txt)

# CI環境ではGitHub Actionsのservicesから、ローカルではdocker-composeのサービス名からURLを取得
# CIのservicesではlocalhostで公開される
API_URL = os.getenv("EXTRACTION_API_URL", "http://extraction:8080")


def test_health_check():
    """
    Tests if the /health endpoint is reachable and returns a 200 OK status.
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        # Assert that the request was successful
        response.raise_for_status()
        # Assert that the response body is as expected
        assert response.json() == {"status": "ok"}
    except requests.exceptions.RequestException as e:
        pytest.fail(
            f"Failed to connect to the extraction service at {API_URL}. Error: {e}"
        )


def test_extract_endpoint_with_sample_pptx():
    """
    Tests the /extract endpoint by uploading a sample PPTX file.
    Asserts that the response is 200 OK and contains the expected JSON structure.
    """
    # Path to the sample file, relative to the project root
    sample_file_path = Path(__file__).parent / "test_sample.pptx"

    assert sample_file_path.exists(), f"Sample file not found at {sample_file_path}"

    try:
        with open(sample_file_path, "rb") as f:
            files = {
                "file": (
                    sample_file_path.name,
                    f,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            }
            response = requests.post(
                f"{API_URL}/document/embed", files=files, timeout=20
            )

        # Assert that the request was successful
        response.raise_for_status()
        data = response.json()

        # Assert the structure of the JSON response
        assert "filename" in data
        assert "message" in data
        assert "slides_processed" in data
        assert data["filename"] == sample_file_path.name

    except requests.exceptions.RequestException as e:
        pytest.fail(
            f"Failed to connect or get a valid response from the /embed endpoint. Error: {e}"
        )


# Contains AI-generated edits.
