import json
import os
import re
import unicodedata
from pinecone import Pinecone, ServerlessSpec
from chromadb.utils import embedding_functions

def main():
    print("Starting Pinecone Ingredients ETL Pipeline...")
    pc_api_key = os.environ.get("PINECONE_API_KEY")
    if not pc_api_key:
        print("CRITICAL ERROR: PINECONE_API_KEY not set.")
        return

    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=pc_api_key)
    index_name = "patchamomma-ingredients"

    if index_name not in pc.list_indexes().names():
        print(f"Creating Pinecone index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    index = pc.Index(index_name)

    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'services', 'detective', 'data')
    root_data_dir = os.path.join(base_dir, '..', 'data')

    print("Loading data files...")
    with open(os.path.join(data_dir, 'additives.json'), 'r') as f: additives_db = json.load(f)
    with open(os.path.join(data_dir, 'ingredients.json'), 'r') as f: ingredients_db = json.load(f)

    ins_categories_db = {}
    if os.path.exists(os.path.join(root_data_dir, 'ins_food_additives.json')):
        with open(os.path.join(root_data_dir, 'ins_food_additives.json'), 'r') as f:
            for item in json.load(f).get("additives", []):
                ins_categories_db[item["ins"].lower()] = item

    print("Initializing embedding model...")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    docs, metadatas, ids = [], [], []

    print("Processing Additives...")
    for key, entry in additives_db.items():
        if not isinstance(entry, dict): continue
        names = entry.get('name', {})
        en_name = names.get('en', '')
        if not en_name: continue
        
        clean_name = re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', en_name, flags=re.IGNORECASE).title()
        code = key.replace('en:e', '').lower()
        ins_cat = ins_categories_db.get(code, {})
        
        raw_cat = ins_cat.get("source", {}).get("category", "")
        if raw_cat == "natural": source = "Natural"
        elif raw_cat == "natural_derived": source = "Natural Derived"
        elif raw_cat == "synthetic/processed": source = "Synthetic / Processed"
        else: source = "Synthetic / Processed"

        risk_raw = entry.get("efsa_evaluation_overexposure_risk", {}).get("en", "")
        risk = "High Risk" if "high" in risk_raw else "Safe" if "low" in risk_raw else "Moderate Risk"
        
        meta = {
            "name": clean_name,
            "ins_code": code.upper(),
            "category": "Additive",
            "source": source,
            "risk_level": risk,
            "explanation": entry.get("description", {}).get("en", ""),
            "is_additive": True
        }
        
        synonyms = set([clean_name.lower()])
        for val in names.values():
            synonyms.add(re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', val, flags=re.IGNORECASE).lower().strip())
        
        synonyms.add(f"ins {code}")
        synonyms.add(f"e{code}")
        
        for i, syn in enumerate(synonyms):
            if not syn: continue
            docs.append(syn)
            metadatas.append(meta)
            raw_id = f"add_{code}_{i}"
            safe_id = unicodedata.normalize("NFKD", raw_id).encode("ASCII", "ignore").decode("utf-8")
            ids.append(safe_id)

    print("Processing Standard Ingredients...")
    for key, entry in ingredients_db.items():
        if not isinstance(entry, dict): continue
        names = entry.get('name', {})
        en_name = names.get('en', '')
        if not en_name: continue
        
        meta = {
            "name": en_name.title(),
            "ins_code": "",
            "category": "Standard Ingredient",
            "source": "Natural",
            "risk_level": "Safe",
            "explanation": entry.get("description", {}).get("en", ""),
            "is_additive": False
        }
        
        synonyms = set([en_name.lower().strip()])
        for val in names.values():
            synonyms.add(val.lower().strip())
            
        for i, syn in enumerate(synonyms):
            if not syn: continue
            docs.append(syn)
            metadatas.append(meta)
            raw_id = f"ing_{key.replace(':', '_')}_{i}"
            safe_id = unicodedata.normalize("NFKD", raw_id).encode("ASCII", "ignore").decode("utf-8")
            safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", safe_id)
            ids.append(safe_id)

    print(f"Embedding and upserting {len(docs)} vectors to Pinecone...")
    batch_size = 100
    start_batch = 228  # Batch 229 failed, so we start at index 228 * 100
    print(f"Resuming from batch {start_batch + 1} to avoid repeating work...")
    
    for i in range(start_batch * batch_size, len(docs), batch_size):
        batch_docs = docs[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        
        # Pinecone metadata values cannot be None/null, ensure everything is a string/bool
        for m in batch_metas:
            for k, v in m.items():
                if v is None:
                    m[k] = ""
                    
        batch_vecs = emb_fn(batch_docs)
        
        upsert_data = []
        for j in range(len(batch_docs)):
            upsert_data.append({
                "id": batch_ids[j],
                "values": batch_vecs[j].tolist() if hasattr(batch_vecs[j], 'tolist') else batch_vecs[j],
                "metadata": batch_metas[j]
            })
            
        index.upsert(vectors=upsert_data)
        print(f"Upserted batch {i//batch_size + 1}")

    print("✅ Ingredients ETL Pipeline completed successfully! Your data is now live on Pinecone.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
