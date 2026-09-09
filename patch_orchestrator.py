import re

with open('backend/services/orchestrator/api/routes.py', 'r') as f:
    content = f.read()

new_route = """
@router.post("/front-scanner")
async def process_front_scanner(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}
        
        async with httpx.AsyncClient() as client:
            extract_res = await client.post("http://127.0.0.1:8000/api/v1/vision/analyze-front", files=files, timeout=60.0)
            if extract_res.status_code != 200:
                err_detail = "Front Extraction failed"
                try: err_detail = extract_res.json().get("detail", err_detail)
                except: pass
                raise HTTPException(status_code=500, detail=err_detail)
            
            return extract_res.json()
    except Exception as e:
        logger.error(f"Front Scanner Orchestration error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
"""

if "/front-scanner" not in content:
    content = content + new_route

with open('backend/services/orchestrator/api/routes.py', 'w') as f:
    f.write(content)
