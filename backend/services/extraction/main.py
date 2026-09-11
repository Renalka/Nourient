from fastapi import FastAPI
import sys
import os

# Ensure the root backend directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.config import settings
from core.cors import configure_cors
from services.extraction.api.routes import router as extraction_router

app = FastAPI(
    title="Nourient - Vision Extraction Service",
    description="Microservice for extracting structured data from food labels using Gemini Vision",
    version="1.0.0"
)

configure_cors(app)

# Mount the extraction routes
app.include_router(extraction_router, prefix="/api/v1/vision", tags=["Vision Extraction"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "extraction",
        "environment": settings.ENVIRONMENT
    }
