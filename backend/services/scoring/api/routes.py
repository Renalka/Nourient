from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.scoring.core.engine import ScoringEngine

logger = logging.getLogger(__name__)

router = APIRouter()
engine = ScoringEngine()

@router.post("/evaluate")
async def evaluate_product(payload: Dict[str, Any]):
    try:
        result = engine.evaluate(payload)
        return result
    except Exception as e:
        logger.error(f"Scoring error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
