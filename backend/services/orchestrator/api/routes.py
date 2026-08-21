from fastapi import APIRouter, HTTPException, UploadFile, File
import httpx
import asyncio
import logging
import traceback

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

router = APIRouter(prefix="/api/v1/orchestrate", tags=["Orchestrator"])

# Internal microservice URLs
EXTRACTION_URL = "http://127.0.0.1:8000/api/v1/vision/extract"
SCORING_URL = "http://127.0.0.1:8001/api/v1/score/calculate"
AUDITOR_URL = "http://127.0.0.1:8002/api/v1/audit/claims"
DETECTIVE_URL = "http://127.0.0.1:8004/api/v1/detective/analyze"
BIOCONTEXT_URL = "http://127.0.0.1:8005/api/v1/biocontext/evaluate"

from fastapi import Form, Depends
from typing import Optional
from core.security import get_current_user_id

@router.post("/scan")
async def process_scan(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """
    Central orchestration endpoint.
    1. Sends image to Extraction API.
    2. Broadcasts extracted JSON concurrently to Scoring, TrueLabel, and Detective APIs.
    3. Calls BioContext with the base score.
    4. Aggregates and returns the unified result.
    """
    try:
        image_bytes = await file.read()
        
        async with httpx.AsyncClient() as client:
            logger.info("Orchestrator: Calling Extraction Microservice...")
            files = {'file': (file.filename, image_bytes, file.content_type)}
            extract_res = await client.post(EXTRACTION_URL, files=files, timeout=120.0)
            
            if extract_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Extraction API Failed")
                
            extracted_data = extract_res.json()
            
            # Concurrently call Scoring, Auditor, and Detective
            score_req = client.post(SCORING_URL, json=extracted_data, timeout=30.0)
            audit_req = client.post(AUDITOR_URL, json=extracted_data, timeout=60.0)
            detective_req = client.post(DETECTIVE_URL, json={"ingredients": extracted_data.get("ingredients", [])}, timeout=30.0)
            
            results = await asyncio.gather(score_req, audit_req, detective_req, return_exceptions=True)
            score_res, audit_res, detective_res = results
            
            score_data = score_res.json() if not isinstance(score_res, Exception) and score_res.status_code == 200 else None
            audit_data = audit_res.json() if not isinstance(audit_res, Exception) and audit_res.status_code == 200 else None
            detective_data = detective_res.json() if not isinstance(detective_res, Exception) and detective_res.status_code == 200 else None

            # Call BioContext only for authenticated users
            bio_data = None
            if score_data and user_id != "anonymous":
                bio_payload = {
                    "user_id": user_id,
                    "product_data": extracted_data,
                    "base_score": score_data.get("nutritional_quality_score", 50)
                }
                bio_res = await client.post(BIOCONTEXT_URL, json=bio_payload, timeout=30.0)
                if bio_res.status_code == 200:
                    bio_data = bio_res.json()

            # Aggregate payload
            unified_response = {
                "extracted_data": extracted_data,
                "score": score_data,
                "audit": audit_data,
                "detective": detective_data,
                "biocontext": bio_data
            }
            
            logger.info("Orchestrator: Workflow complete.")
            return unified_response

    except Exception as e:
        logger.error(f"Orchestrator CRITICAL ERROR: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
