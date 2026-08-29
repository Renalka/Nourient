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
SCORING_URL = "http://127.0.0.1:8001/api/v1/score/evaluate"
AUDITOR_URL = "http://127.0.0.1:8002/api/v1/audit/claims"
DETECTIVE_URL = "http://127.0.0.1:8004/api/v1/detective/analyze"
BIOCONTEXT_URL = "http://127.0.0.1:8005/api/v1/biocontext/evaluate"

from fastapi import Form, Depends
from typing import Optional
from core.security import get_current_user_id

@router.post("/scanner")
async def process_scanner(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """
    Optimized route for the Vision Scanner & Score module.
    Calls Extraction -> Scoring -> Detective -> BioContext.
    """
    try:
        # 1. Extraction (Sequential because others depend on it)
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}
        
        async with httpx.AsyncClient() as client:
            extract_res = await client.post(EXTRACTION_URL, files=files, timeout=60.0)
            if extract_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Extraction failed")
            
            extracted_data = extract_res.json()

            # 2. Concurrently call Scoring and Detective
            tasks = [
                client.post(SCORING_URL, json=extracted_data, timeout=30.0),
                client.post(DETECTIVE_URL, json={"ingredients": extracted_data.get("ingredients", [])}, timeout=30.0)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            score_res, detective_res = results
            score_data = score_res.json() if not isinstance(score_res, Exception) and score_res.status_code == 200 else None
            detective_data = detective_res.json() if not isinstance(detective_res, Exception) and detective_res.status_code == 200 else None

            # 3. Call BioContext only for authenticated users
            bio_data = None
            if score_data and user_id != "anonymous":
                # Master Score = Average of Macros (Nutri-Score) + Processing (NOVA ML)
                master_score = int((score_data.get("nutritional_quality_score", 50) + score_data.get("processing_score", 50)) / 2)
                bio_payload = {
                    "user_id": user_id,
                    "product_data": extracted_data,
                    "base_score": master_score
                }
                bio_res = await client.post(BIOCONTEXT_URL, json=bio_payload, timeout=30.0)
                if bio_res.status_code == 200:
                    bio_data = bio_res.json()

            return {
                "extracted_data": extracted_data,
                "score": score_data,
                "detective": detective_data,
                "biocontext": bio_data
            }

    except Exception as e:
        logger.error(f"Scanner Orchestration error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auditor")
async def process_auditor(
    file: UploadFile = File(...)
):
    """
    Optimized route for the TrueLabel Auditor module.
    Calls Extraction -> Auditor. Ignores scoring and biocontext.
    """
    try:
        # 1. Extraction
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}
        
        async with httpx.AsyncClient() as client:
            extract_res = await client.post(EXTRACTION_URL, files=files, timeout=60.0)
            if extract_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Extraction failed")
            
            extracted_data = extract_res.json()

            # 2. Call Auditor
            audit_res = await client.post(AUDITOR_URL, json=extracted_data, timeout=45.0)
            
            audit_data = audit_res.json() if audit_res.status_code == 200 else None

            return {
                "extracted_data": extracted_data,
                "audit": audit_data
            }

    except Exception as e:
        logger.error(f"Auditor Orchestration error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
