from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel
from typing import List
from services.detective.core.bq_lookup import DetectiveService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/detective", tags=["Ingredient Detective"])
detective = DetectiveService()

class IngredientPayload(BaseModel):
    ingredients: List[str]

@router.post("/analyze")
async def analyze_ingredients(payload: IngredientPayload):
    try:
        logger.info(f"Analyzing {len(payload.ingredients)} ingredients...")
        flagged = detective.analyze_ingredients(payload.ingredients)
        logger.info(f"Detective flagged {len(flagged)} complex ingredients.")
        return {"flagged_ingredients": flagged}
    except Exception as e:
        logger.error(f"Detective failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
