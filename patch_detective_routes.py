import re

with open('backend/services/detective/api/routes.py', 'r') as f:
    content = f.read()

imports = """
from pydantic import BaseModel
from typing import List, Dict, Any
from services.detective.core.claims_engine import ClaimsEngine

claims_engine = ClaimsEngine()

class ClaimsVerificationRequest(BaseModel):
    explicit_claims: List[str]
    ingredients: List[Dict[str, Any]]

@router.post("/verify-claims")
async def verify_claims(req: ClaimsVerificationRequest):
    try:
        result = claims_engine.verify(req.explicit_claims, req.ingredients)
        return result
    except Exception as e:
        logger.error(f"Error in verify-claims: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
"""

content = content + "\n" + imports

with open('backend/services/detective/api/routes.py', 'w') as f:
    f.write(content)

