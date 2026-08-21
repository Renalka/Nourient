from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from core.models.product import ExtractedProductData, TrueLabelAuditResult
from services.auditor.core.agent import AuditorAgent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

router = APIRouter(prefix="/api/v1/audit", tags=["TrueLabel Auditor"])
agent = AuditorAgent()

@router.post("/claims", response_model=TrueLabelAuditResult)
async def audit_claims(product: ExtractedProductData):
    """
    Takes an extracted product and audits its marketing claims against its ingredients.
    """
    try:
        logger.info(f"Auditing claims for: {product.name}")
        audit_result = await agent.audit_product(product)
        logger.info(f"Audit complete. Trust Score: {audit_result.overall_trust_score}")
        return audit_result
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")
