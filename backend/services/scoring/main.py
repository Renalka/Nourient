from fastapi import FastAPI
import sys
import os

# Ensure the root backend directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.config import settings
from core.cors import configure_cors
from services.scoring.api.routes import router as scoring_router

app = FastAPI(
    title="Nourient - Scoring Service",
    description="Microservice for calculating Food Decision Profiles",
    version="1.0.0"
)

configure_cors(app)

app.include_router(scoring_router, prefix="/api/v1/score", tags=["Scoring"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "scoring",
        "environment": settings.ENVIRONMENT
    }
