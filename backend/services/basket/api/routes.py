from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel
from typing import Dict, Any
from services.basket.core.engine import BasketEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/basket", tags=["Basket Intelligence"])
engine = BasketEngine()

class AddItemPayload(BaseModel):
    user_id: str
    product_data: Dict[str, Any]

@router.post("/add")
async def add_item(payload: AddItemPayload):
    try:
        engine.add_to_basket(payload.user_id, payload.product_data)
        return {"status": "success", "message": "Item added to basket."}
    except Exception as e:
        logger.error(f"Failed to add to basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/{user_id}")
async def analyze(user_id: str):
    try:
        analysis = engine.analyze_basket(user_id)
        return analysis
    except Exception as e:
        logger.error(f"Failed to analyze basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear/{user_id}")
async def clear(user_id: str):
    try:
        engine.clear_basket(user_id)
        return {"status": "success", "message": "Basket cleared."}
    except Exception as e:
        logger.error(f"Failed to clear basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove/{user_id}/{index}")
async def remove(user_id: str, index: int):
    try:
        engine.remove_item(user_id, index)
        return {"status": "success", "message": "Item removed from basket."}
    except Exception as e:
        logger.error(f"Failed to remove item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
