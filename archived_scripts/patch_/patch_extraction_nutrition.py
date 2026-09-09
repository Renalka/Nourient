import re

with open('backend/services/extraction/api/routes.py', 'r') as f:
    content = f.read()

if 'from core.models.product import ExtractedProductData' in content:
    content = content.replace(
        'from core.models.product import ExtractedProductData, FrontOfPackData',
        'from core.models.product import ExtractedProductData, FrontOfPackData, NutritionExtractionData'
    )

new_route = """

NUTRITION_PANEL_PROMPT = \"\"\"
You are a highly accurate food nutrition extraction AI.
Analyze the provided image of a food product's NUTRITION FACTS panel.
Extract the tabular data and serving size explicitly. 

Return strictly in the following JSON format:
{
  "stated_serving": {
    "amount": 30.0,
    "unit": "g",
    "description": "e.g. 1/4 cookie or 2 biscuits"
  },
  "raw_table": {
    "calories_per_100g": 0.0,
    "sugar_per_100g": 0.0,
    "fiber_per_100g": 0.0,
    "protein_per_100g": 0.0,
    "sodium_per_100g": 0.0,
    "fat_per_100g": 0.0,
    "sat_fat_per_100g": 0.0
  },
  "error": null,
  "error_message": null
}

CRITICAL INSTRUCTIONS:
1. You MUST extract values strictly "per 100g" or "per 100ml" for the raw_table. If the table ONLY shows per serving, calculate the per 100g values mathematically based on the serving size amount.
2. Ensure the stated serving is what the manufacturer claims is one serving.
3. If no nutrition table is found, set error to "INVALID_IMAGE" and error_message to "Could not detect a nutrition table."
\"\"\"

@router.post("/analyze-nutrition", response_model=NutritionExtractionData)
async def analyze_nutrition_panel(file: UploadFile = File(...)):
    logger.info(f"Incoming POST request to /analyze-nutrition with file: {file.filename}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image type (jpeg, png, etc).")
        
    try:
        image_bytes = await file.read()
        logger.info(f"Sending nutrition image to Gemini... Size: {len(image_bytes)} bytes.")
        
        extracted_data = await ai_engine.extract_structured_data(
            image_bytes=image_bytes,
            prompt=NUTRITION_PANEL_PROMPT
        )
        
        product_model = NutritionExtractionData(**extracted_data)
        logger.info("Nutrition panel extraction complete.")
        return product_model
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR during nutrition extraction: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Nutrition Extraction failed: {str(e)}")
"""

content = content + new_route

with open('backend/services/extraction/api/routes.py', 'w') as f:
    f.write(content)

