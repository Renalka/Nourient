import json
import os
import re
import chromadb
from chromadb.utils import embedding_functions

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '..', 'services', 'detective', 'data')
root_data_dir = os.path.join(base_dir, '..', 'data')
db_path = os.path.join(base_dir, '..', 'data', 'chroma_db')

client = chromadb.PersistentClient(path=db_path)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

try: client.delete_collection("ingredients")
except Exception: pass

collection = client.create_collection("ingredients", embedding_function=emb_fn)

with open(os.path.join(data_dir, 'additives.json'), 'r') as f: additives_db = json.load(f)
with open(os.path.join(data_dir, 'ingredients.json'), 'r') as f: ingredients_db = json.load(f)

ins_categories_db = {}
if os.path.exists(os.path.join(root_data_dir, 'ins_food_additives.json')):
    with open(os.path.join(root_data_dir, 'ins_food_additives.json'), 'r') as f:
        for item in json.load(f).get("additives", []):
            ins_categories_db[item["ins"].lower()] = item

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
    
    # Metadata construction (same as before)
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
    
    # Insert multiple vectors for this one ingredient
    synonyms = set([clean_name.lower()])
    for val in names.values():
        synonyms.add(re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', val, flags=re.IGNORECASE).lower().strip())
    
    synonyms.add(f"ins {code}")
    synonyms.add(f"e{code}")
    
    for i, syn in enumerate(synonyms):
        if not syn: continue
        docs.append(syn)
        metadatas.append(meta)
        ids.append(f"add_{code}_{i}")

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
        ids.append(f"ing_{key.replace(':', '_')}_{i}")

print(f"Adding {len(docs)} vectors to ChromaDB...")
batch_size = 5000
for i in range(0, len(docs), batch_size):
    collection.add(documents=docs[i:i+batch_size], metadatas=metadatas[i:i+batch_size], ids=ids[i:i+batch_size])
    print(f"Inserted batch {i//batch_size + 1}")

print("Done building V2 Vector DB!")
