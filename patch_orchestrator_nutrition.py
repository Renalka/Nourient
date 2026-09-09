import re

with open('backend/services/orchestrator/api/routes.py', 'r') as f:
    content = f.read()

new_route = """
@router.post("/nutrition-scanner")
async def process_nutrition_scanner(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}
        
        async with httpx.AsyncClient() as client:
            # 1. Vision extraction of the nutrition table
            extract_res = await client.post("http://127.0.0.1:8000/api/v1/vision/analyze-nutrition", files=files, timeout=60.0)
            if extract_res.status_code != 200:
                err_detail = "Nutrition Extraction failed"
                try: err_detail = extract_res.json().get("detail", err_detail)
                except: pass
                raise HTTPException(status_code=500, detail=err_detail)
                
            extracted_data = extract_res.json()
            
            # 2. Nutrition Math Heuristics Engine
            math_res = await client.post("http://127.0.0.1:8008/api/v1/nutrition/analyze", json=extracted_data, timeout=30.0)
            if math_res.status_code != 200:
                err_detail = "Nutrition Math Engine failed"
                try: err_detail = math_res.json().get("detail", err_detail)
                except: pass
                raise HTTPException(status_code=500, detail=err_detail)
            
            return math_res.json()
    except Exception as e:
        logger.error(f"Nutrition Scanner Orchestration error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
"""

if "/nutrition-scanner" not in content:
    content = content + new_route

with open('backend/services/orchestrator/api/routes.py', 'w') as f:
    f.write(content)
