import logging

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Extraction Service",
    description="Extracts content from presentation files.",
    version="0.1.0",
)


@app.get("/health", summary="Health Check")
def health_check():
    """
    Simple health check endpoint to confirm the service is running.
    """
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}


@app.post("/extract", summary="Extract Content from PPTX")
async def extract_content(file: UploadFile = File(...)):
    """
    (Placeholder) Endpoint to extract content from an uploaded PPTX file.
    In a real implementation, this would use exparso to process the file.
    """
    logger.info(f"Received file: {file.filename} of type {file.content_type}")
    # This is a placeholder response.
    # The actual extraction logic will be implemented later.
    return JSONResponse(
        status_code=200,
        content={
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "File received, processing logic not yet implemented.",
            "slides": [],  # Placeholder for extracted data
        },
    )


# Contains AI-generated edits.
