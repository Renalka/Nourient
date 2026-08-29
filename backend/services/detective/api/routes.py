from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel
from typing import List
from services.detective.core.bq_lookup import DetectiveService
from services.detective.core.ins_decoder import IngredientDecoder

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/detective", tags=["Ingredient Detective"])
detective = DetectiveService()
decoder = IngredientDecoder()

class IngredientPayload(BaseModel):
    ingredients: List[dict]

@router.post("/analyze")
async def analyze_ingredients(payload: IngredientPayload):
    try:
        logger.info(f"Analyzing {len(payload.ingredients)} ingredients...")
        
        # 1. BigQuery Flagger (for complex ingredients without INS codes)
        flagged = detective.analyze_ingredients(payload.ingredients)
        
        # 2. Deterministic Unified Decoder (Additives + Standard Ingredients)
        decoded_additives = decoder.decode_ingredients(payload.ingredients)
        
        logger.info(f"Detective found {len(flagged)} complex items and decoded {len(decoded_additives)} INS additives.")
        
        return {
            "flagged_ingredients": flagged,
            "decoded_additives": decoded_additives
        }
    except Exception as e:
        logger.error(f"Detective failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
