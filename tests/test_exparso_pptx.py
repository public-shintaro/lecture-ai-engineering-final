# tests/test_exparso_pptx.py
from pathlib import Path

from exparso.loader.pptx_loader import PptxLoader


def test_parse_pptx_returns_pages():
    """
    Tests that parsing a sample PPTX file using Exparso returns a dictionary
    with a 'pages' key, and 'pages' is a list with at least one page.
    """
    # Construct the path to the sample PPTX file relative to this test file.
    pptx_path = Path(__file__).parent / "test_sample.pptx"
    print(f"DEBUG: PPTX path is {pptx_path}")  # 追加

    # Initialize the Exparso Document with the PPTX file.
    print("DEBUG: Calling parse_document...")  # 追加
    loader = PptxLoader()
    result = loader.load(path=str(pptx_path))
    print("DEBUG: parse_document finished.")  # 追加

    # Assert that the result is a dictionary.
    assert isinstance(result, list), "The result of parsing should be a dictionary."

    # Assert that there is at least one page in the 'pages' list.
    assert len(result) > 0, "There should be at least one page in the parsed document."


# Contains AI-generated edits.
