from fastapi import FastAPI
# Note: When running from the backend root, imports will be relative to it
from core.config import settings

app = FastAPI(
    title="Nourient - Scoring Service",
    description="Microservice for calculating Food Decision Profiles and Contextual Scores",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "scoring",
        "environment": settings.ENVIRONMENT
    }

# We will mount routers here later
# from services.scoring.api.routes import router
# app.include_router(router, prefix="/api/v1/score")
