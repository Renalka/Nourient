from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.nutrition.api.routes import router as nutrition_router
from core.cors import configure_cors

app = FastAPI(title="Nourient - Nutrition Heuristics Service")

configure_cors(app)

app.include_router(nutrition_router, prefix="/api/v1/nutrition", tags=["Nutrition Engine"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nutrition"}
