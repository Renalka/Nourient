from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel
from typing import Dict, Any, List
from services.alternatives.core.engine import AlternativesEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/alternatives", tags=["Alternatives"])
engine = AlternativesEngine()

class AlternativeRequest(BaseModel):
    category: str
    current_sugar: float = 0.0
    current_protein: float = 0.0

@router.post("/find")
async def find_alternatives(payload: AlternativeRequest):
    try:
        logger.info(f"Finding alternatives for category: {payload.category}")
        results = engine.find_better_alternatives(
            payload.category,
            payload.current_sugar,
            payload.current_protein
        )
        return {"alternatives": results}
    except Exception as e:
        logger.error(f"Alternatives failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
