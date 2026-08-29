from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel
from typing import Dict, Any
from services.biocontext.core.engine import BioContextEngine, BioContextResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/biocontext", tags=["BioContext"])
engine = BioContextEngine()

class BioContextPayload(BaseModel):
    user_id: str
    product_data: Dict[str, Any]
    base_score: int

@router.post("/evaluate", response_model=BioContextResult)
async def evaluate_context(payload: BioContextPayload):
    try:
        logger.info(f"Evaluating BioContext for user {payload.user_id}")
        result = engine.calculate_fit(payload.user_id, payload.product_data, payload.base_score)
        logger.info(f"BioContext fit: {result.metabolic_fit_score}")
        return result
    except Exception as e:
        logger.error(f"BioContext failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ProfileUpdatePayload(BaseModel):
    user_id: str
    health_profile: str

@router.post("/update_profile")
async def update_profile(payload: ProfileUpdatePayload):
    try:
        engine.update_user_profile(payload.user_id, payload.health_profile)
        return {"status": "success", "message": f"Updated profile to {payload.health_profile}"}
    except Exception as e:
        logger.error(f"Failed to update profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))
