from fastapi import APIRouter, HTTPException, Depends
import logging
from pydantic import BaseModel
from typing import Dict, Any
from services.basket.core.engine import BasketEngine
from core.security import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/basket", tags=["Basket Intelligence"])
engine = BasketEngine()

class AddItemPayload(BaseModel):
    product_data: Dict[str, Any]

@router.post("/add")
async def add_item(payload: AddItemPayload, uid: str = Depends(get_current_user_id)):
    try:
        engine.add_to_basket(uid, payload.product_data)
        return {"status": "success", "message": "Item added to basket."}
    except Exception as e:
        logger.error(f"Failed to add to basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze")
async def analyze(uid: str = Depends(get_current_user_id)):
    try:
        analysis = engine.analyze_basket(uid)
        return analysis
    except Exception as e:
        logger.error(f"Failed to analyze basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear")
async def clear(uid: str = Depends(get_current_user_id)):
    try:
        engine.clear_basket(uid)
        return {"status": "success", "message": "Basket cleared."}
    except Exception as e:
        logger.error(f"Failed to clear basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove/{index}")
async def remove(index: int, uid: str = Depends(get_current_user_id)):
    try:
        engine.remove_item(uid, index)
        return {"status": "success", "message": "Item removed from basket."}
    except Exception as e:
        logger.error(f"Failed to remove item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
