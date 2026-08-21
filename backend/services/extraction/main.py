from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Ensure the root backend directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.config import settings
from services.extraction.api.routes import router as extraction_router

app = FastAPI(
    title="Nourient - Vision Extraction Service",
    description="Microservice for extracting structured data from food labels using Gemini Vision",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], # Allow local frontend development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the extraction routes
app.include_router(extraction_router, prefix="/api/v1/vision", tags=["Vision Extraction"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "extraction",
        "environment": settings.ENVIRONMENT
    }
