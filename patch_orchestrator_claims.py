import re

with open('backend/services/orchestrator/api/routes.py', 'r') as f:
    content = f.read()

new_route = """
@router.post("/claims-scanner")
async def process_claims_scanner(front_file: UploadFile = File(...), back_file: UploadFile = File(...)):
    try:
        front_bytes = await front_file.read()
        back_bytes = await back_file.read()
        
        async with httpx.AsyncClient() as client:
            # 1. Extract Front Claims
            f_files = {"file": (front_file.filename, front_bytes, front_file.content_type)}
            front_res = await client.post("http://127.0.0.1:8000/api/v1/vision/analyze-front", files=f_files, timeout=60.0)
            if front_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Front extraction failed")
            front_data = front_res.json()
            explicit_claims = front_data.get("explicit_claims", [])
            
            # 2. Extract Back Ingredients
            b_files = {"file": (back_file.filename, back_bytes, back_file.content_type)}
            back_res = await client.post("http://127.0.0.1:8000/api/v1/vision/analyze", files=b_files, timeout=60.0)
            if back_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Back extraction failed")
            back_data = back_res.json()
            raw_ingredients = back_data.get("ingredients", [])
            
            # 3. Decode Ingredients
            dec_res = await client.post("http://127.0.0.1:8004/api/v1/detective/decode", json={"ingredients": raw_ingredients}, timeout=30.0)
            if dec_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Decoding failed")
            decoded_ingredients = dec_res.json()
            
            # 4. Verify Claims
            verify_payload = {
                "explicit_claims": explicit_claims,
                "ingredients": decoded_ingredients
            }
            ver_res = await client.post("http://127.0.0.1:8004/api/v1/detective/verify-claims", json=verify_payload, timeout=30.0)
            if ver_res.status_code != 200:
                raise HTTPException(status_code=500, detail="Verification failed")
                
            return {
                "explicit_claims": explicit_claims,
                "verification": ver_res.json()
            }
            
    except Exception as e:
        logger.error(f"Claims Scanner Orchestration error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
"""

if "/claims-scanner" not in content:
    content = content + new_route

with open('backend/services/orchestrator/api/routes.py', 'w') as f:
    f.write(content)

