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
  "ingredients": [
    {
      "name": "Clean Ingredient Name",
      "ins_code": "INS 330 or E330 or null if not an additive code",
      "percentage": 10.5
    }
  ],
  "claims": ["claim 1", "claim 2"],
  "nutrition": {
    "calories": {"amount": 0, "unit": "kcal"},
    "protein": {"amount": 0.0, "unit": "g"},
    "carbohydrates": {"amount": 0.0, "unit": "g"},
    "sugar": {"amount": 0.0, "unit": "g"},
    "fiber": {"amount": 0.0, "unit": "g"},
    "sodium": {"amount": 0.0, "unit": "mg"},
    "saturated_fat": {"amount": 0.0, "unit": "g"}
  },
  "error": null,
  "error_message": null
}

CRITICAL INSTRUCTIONS FOR REJECTING INVALID IMAGES:
1. If the image is extremely blurry and completely illegible, set `error` to "BLURRY" and `error_message` to "The image is too blurry to read. Please capture a clearer photo of the label."
2. If the image is not a food product label, ingredients list, or nutrition table (e.g., a photo of a person, a random object, scenery), set `error` to "INVALID_IMAGE" and `error_message` to "This does not appear to be a food product label. Please scan the ingredients or nutrition facts."
3. If the image is a food label but contains zero ingredients AND zero nutrition facts, set `error` to "NO_DATA_FOUND" and `error_message` to "We couldn't detect any ingredients or nutrition facts. Ensure the text is clearly visible."
4. If you set an error, leave the other fields (name, brand, ingredients, claims) empty or empty lists.

CRITICAL INSTRUCTIONS FOR INGREDIENTS:
1. Extract a clean, deduplicated list of ingredients.
2. If an ingredient has a quantity (like percentages mentioned in brackets e.g. "Wheat Flour (60%)"), extract the percentage value as a float.
3. If an ingredient contains an INS code or E-number (e.g. "Acidity Regulator (INS 330)"), put "INS 330" in `ins_code` and put "Acidity Regulator" in `name`. Do not leave the INS code inside the name.
4. If an ingredient groups a generic category with a specific ingredient (e.g., "Emulsifier - Soy Lecithin", "Emulsifier (Soy Lecithin)", "Flavoring (Vanilla)", "Vegetable Oil (Palm Oil)"), you MUST extract the SPECIFIC ingredient as the `name` (e.g. "Soy Lecithin", "Vanilla", "Palm Oil"). Do NOT use the generic category (Emulsifier, Flavoring, Vegetable Oil) as the primary name, unless there is no specific ingredient mentioned.

CRITICAL INSTRUCTIONS FOR NUTRITION FACTS:
1. You MUST extract values strictly "per 100g" or "per 100ml". 
2. If the nutrition table has multiple columns (e.g., "Per Serving" and "Per 100g"), you MUST ONLY look at the "Per 100g" column. Ignore the serving column completely to avoid confusion.
3. If the label ONLY shows "Per Serving" (e.g. per 30g), you MUST mathematically convert the values to 100g (e.g. multiply by 3.33) and return the 100g values.
4. For sugar, extract Total Sugars. 
5. If a specific nutrition value is completely missing, use {"amount": 0, "unit": ""} for it.
Do not hallucinate. Return ONLY valid JSON.
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
