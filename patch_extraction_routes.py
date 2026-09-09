import re

with open('backend/services/extraction/api/routes.py', 'r') as f:
    content = f.read()

if 'from core.models.product import ExtractedProductData' in content:
    content = content.replace(
        'from core.models.product import ExtractedProductData',
        'from core.models.product import ExtractedProductData, FrontOfPackData'
    )

new_route = """

FRONT_PACK_PROMPT = \"\"\"
You are a highly analytical food marketing and psychology AI expert.
Analyze the provided image of the FRONT of a food product's packaging.
Your goal is to detect the "Health Halo" effect, target audience, and misleading prominent ingredients.

Return strictly in the following JSON format:
{
  "health_halo": {
    "visual_cues": ["list of visual tricks, e.g. rustic fonts, green leaves, earthy tones"],
    "deception_index": 85,
    "reasoning": "Explanation of how the visual vibe contrasts with the likely reality of the product"
  },
  "target_audience": {
    "demographic": "e.g. Children, Athletes, Health-conscious adults",
    "indicators": ["cartoon mascots", "bright primary colors"],
    "concerns": ["If aimed at kids, flag concerns about synthetic dyes. If aimed at athletes, flag hidden sugars"]
  },
  "prominent_ingredients": [
    {
      "name": "e.g. Real Strawberries",
      "implied_quantity": "Showcased as the primary ingredient via massive imagery",
      "reality_check": "Often makes up < 1% of the formulation. Check the ingredients list to verify."
    }
  ],
  "error": null,
  "error_message": null
}

CRITICAL INSTRUCTIONS:
1. 'deception_index' should be 0-100, where 100 means highly deceptive visual marketing (e.g. junk food disguised as health food using green washing).
2. Only populate 'prominent_ingredients' if the packaging explicitly showcases a premium ingredient (like fruit, honey, oats) using large text or pictures.
3. If the image is not a food product (e.g., it's a car, a face), set `error` to "INVALID_IMAGE" and `error_message` to "This does not appear to be the front of a food package."
\"\"\"

@router.post("/analyze-front", response_model=FrontOfPackData)
async def analyze_front_pack(file: UploadFile = File(...)):
    logger.info(f"Incoming POST request to /analyze-front with file: {file.filename}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image type (jpeg, png, etc).")
        
    try:
        image_bytes = await file.read()
        logger.info(f"Sending front image to Gemini... Size: {len(image_bytes)} bytes.")
        
        extracted_data = await ai_engine.extract_structured_data(
            image_bytes=image_bytes,
            prompt=FRONT_PACK_PROMPT
        )
        
        product_model = FrontOfPackData(**extracted_data)
        logger.info("Front-of-pack analysis complete.")
        return product_model
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR during front analysis: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Front Analysis failed: {str(e)}")
"""

content = content + new_route

with open('backend/services/extraction/api/routes.py', 'w') as f:
    f.write(content)

