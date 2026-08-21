from fastapi import APIRouter, UploadFile, File, HTTPException
import sys
import os
import traceback
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ExtractionRouter")

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.models.product import ExtractedProductData
from services.extraction.core.ai_engine import GeminiEngine

router = APIRouter()

logger.info("Initializing Gemini Engine...")
try:
    ai_engine = GeminiEngine()
except Exception as e:
    logger.error(f"Failed to initialize GeminiEngine: {e}")

# The system prompt enforcing the extraction rules and the strict JSON schema
EXTRACTION_PROMPT = """
You are a highly accurate food nutrition extraction AI.
Analyze the provided image of a food product's packaging (ingredients list, nutrition table, or front cover).
Extract the details meticulously and return them strictly in the following JSON format:

{
  "name": "Product Name (or empty string)",
  "brand": "Brand Name (or empty string)",
  "category": "Category like Cereal, Snack, etc (or empty string)",
  "price": null,
  "ingredients": ["ingredient 1", "ingredient 2"],
  "claims": ["claim 1", "claim 2"],
  "nutrition": {
    "calories": {"amount": 0, "unit": "kcal"},
    "protein": {"amount": 0.0, "unit": "g"},
    "carbohydrates": {"amount": 0.0, "unit": "g"},
    "added_sugar": {"amount": 0.0, "unit": "g"},
    "fiber": {"amount": 0.0, "unit": "g"},
    "sodium": {"amount": 0.0, "unit": "mg"},
    "saturated_fat": {"amount": 0.0, "unit": "g"}
  }
}

If a specific nutrition value is not visible, use {"amount": 0, "unit": ""} for it.
Always attempt to normalize values to per 100g if both serving and 100g are visible.
Do not hallucinate or guess. Return ONLY valid JSON.
"""

@router.post("/extract", response_model=ExtractedProductData)
async def extract_label_data(file: UploadFile = File(...)):
    logger.info(f"Incoming POST request to /extract with file: {file.filename}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image type (jpeg, png, etc).")
        
    try:
        image_bytes = await file.read()
        logger.info(f"Successfully read image bytes. Size: {len(image_bytes)} bytes. Sending to Gemini...")
        
        extracted_data = await ai_engine.extract_structured_data(
            image_bytes=image_bytes,
            prompt=EXTRACTION_PROMPT
        )
        
        # Hydrate the raw AI dict into our Pydantic model for type safety
        product_model = ExtractedProductData(**extracted_data)
        
        # Pass the AI output through the BigQuery Ground Truth pipeline
        # If the product exists in the DB, it will overwrite the OCR with hard facts.
        try:
            from core.bq_client import BigQueryService
            bq_service = BigQueryService()
            product_model = bq_service.enrich_product_data(product_model)
            logger.info("Successfully checked BigQuery Ground Truth Database.")
        except Exception as bq_e:
            logger.error(f"BigQuery enrichment failed, falling back to pure AI OCR: {bq_e}")
        
        logger.info("Gemini extraction and enrichment complete.")
        return product_model
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR during extraction: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"AI Extraction failed: {str(e)}")
