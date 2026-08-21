from fastapi import APIRouter
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.models.product import ExtractedProductData, FoodDecisionProfile
from services.scoring.core.scorer import ScoringEngine

router = APIRouter()
scorer = ScoringEngine()

@router.post("/calculate", response_model=FoodDecisionProfile)
async def calculate_profile(product: ExtractedProductData):
    """
    Accepts extracted product data and returns a calculated Food Decision Profile.
    """
    return scorer.calculate_score(product)
