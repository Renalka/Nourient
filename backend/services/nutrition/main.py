from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.nutrition.api.routes import router as nutrition_router

app = FastAPI(title="Nourient - Nutrition Heuristics Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nutrition_router, prefix="/api/v1/nutrition", tags=["Nutrition Engine"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nutrition"}
