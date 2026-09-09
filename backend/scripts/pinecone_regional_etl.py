import json
import os
import re
import unicodedata
from pinecone import Pinecone
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("Starting Regional Ingredients ETL Pipeline...")
    pc_api_key = os.environ.get("PINECONE_API_KEY")
    if not pc_api_key:
        print("CRITICAL ERROR: PINECONE_API_KEY not set.")
        return

    pc = Pinecone(api_key=pc_api_key)
    index = pc.Index("patchamomma-ingredients")

    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, '..', 'services', 'detective', 'data', 'regional_ingredients.json')
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    docs, metadatas, ids = [], [], []

    for item in data.get("regional_terms", []):
        term = item["term"].lower()
        english = item["english_name"]
        
        meta = {
            "name": english,
            "ins_code": "",
            "category": item["category"],
            "source": item["source"],
            "risk_level": item["risk_level"],
            "explanation": item["explanation"],
            "is_additive": False
        }
        
        # We will embed the regional term (e.g. "maida") so the vector DB catches it
        docs.append(term)
        metadatas.append(meta)
        
        raw_id = f"reg_{term.replace(' ', '_')}"
        safe_id = unicodedata.normalize("NFKD", raw_id).encode("ASCII", "ignore").decode("utf-8")
        safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", safe_id)
        ids.append(safe_id)

    print(f"Embedding and upserting {len(docs)} regional terms to Pinecone...")
    
    # Pinecone metadata values cannot be None/null
    for m in metadatas:
        for k, v in m.items():
            if v is None:
                m[k] = ""
                
    batch_vecs = emb_fn(docs)
    
    upsert_data = []
    for j in range(len(docs)):
        upsert_data.append({
            "id": ids[j],
            "values": batch_vecs[j].tolist() if hasattr(batch_vecs[j], 'tolist') else batch_vecs[j],
            "metadata": metadatas[j]
        })
        
    index.upsert(vectors=upsert_data)
    print("✅ Regional Ingredients successfully added to Pinecone!")

if __name__ == "__main__":
    main()
