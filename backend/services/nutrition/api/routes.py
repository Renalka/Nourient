from fastapi import APIRouter, HTTPException
import logging
from core.models.product import NutritionExtractionData, NutritionAnalysisData
from services.nutrition.core.engine import NutritionEngine

logger = logging.getLogger("NutritionRouter")
router = APIRouter()
engine = NutritionEngine()

@router.post("/analyze", response_model=NutritionAnalysisData)
async def analyze_nutrition(data: NutritionExtractionData):
    try:
        result = engine.analyze(data)
        return result
    except Exception as e:
        logger.error(f"Error in nutrition math engine: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
