from fastapi import FastAPI

from backend.api.v1.upload import router as upload_router

app = FastAPI(
    title="Lecture-Slide Helper API",
    version="0.1.0",
)

app.include_router(upload_router, prefix="/api")
