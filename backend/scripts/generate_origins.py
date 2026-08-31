import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv("../.env")
api_key = os.environ.get("GEMINI_API_KEY")

def get_origins():
    print("Starting...", flush=True)
    with open("../services/detective/data/additives.json", "r") as f:
        additives_db = json.load(f)
        
    e_numbers = [k for k in additives_db.keys() if k.startswith("en:e")]
    print(f"Total E-numbers found: {len(e_numbers)}", flush=True)
    
    chunk_size = 150
    chunks = [e_numbers[i:i + chunk_size] for i in range(0, len(e_numbers), chunk_size)]
    
    final_dict = {}
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...", flush=True)
        
        prompt = f"""You are a world-class food chemist and regulatory expert. 
Categorize the following list of E-numbers (food additives) into one of these strict categories based on their origin and manufacturing process:
- "Natural" (e.g. beeswax, unadulterated plant extracts)
- "Natural Derived" (e.g. citric acid from fermentation, pectin from apples, modified starches if minimally processed)
- "Synthetic / Processed" (e.g. artificial azo dyes, aspartame, highly processed chemical compounds)
- "Unknown" (if you truly do not know)

CRITICAL INSTRUCTIONS:
Return ONLY a valid, raw JSON object mapping the exact string to its category. Do NOT wrap it in ```json blocks. 
List of E-numbers to categorize: {json.dumps(chunk)}
"""
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        try:
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
                json=payload, timeout=30
            )
            resp.raise_for_status()
            text = resp.json()['candidates'][0]['content']['parts'][0]['text']
            
            parsed = json.loads(text)
            final_dict.update(parsed)
            print(f"Successfully mapped {len(parsed)} additives.", flush=True)
        except Exception as e:
            print(f"Failed chunk {i+1}: {e}", flush=True)
            try:
                print(resp.text)
            except:
                pass
            
        time.sleep(2)
        
    out_path = "../services/detective/data/chemical_origins.json"
    with open(out_path, "w") as f:
        json.dump(final_dict, f, indent=2)
    print(f"Finished! Wrote {len(final_dict)} mappings to {out_path}", flush=True)

if __name__ == "__main__":
    get_origins()
