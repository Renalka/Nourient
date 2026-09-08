import json
import os
import re
import chromadb
from chromadb.utils import embedding_functions

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '..', 'services', 'detective', 'data')
root_data_dir = os.path.join(base_dir, '..', 'data')

db_path = os.path.join(base_dir, '..', 'data', 'chroma_db')
os.makedirs(db_path, exist_ok=True)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=db_path)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# We will create one collection for ingredients
try:
    client.delete_collection("ingredients")
except Exception:
    pass
collection = client.create_collection("ingredients", embedding_function=emb_fn)

additives_path = os.path.join(data_dir, 'additives.json')
ingredients_path = os.path.join(data_dir, 'ingredients.json')
ins_categories_path = os.path.join(root_data_dir, 'ins_food_additives.json')

with open(additives_path, 'r', encoding='utf-8') as f:
    additives_db = json.load(f)

ins_categories_db = {}
if os.path.exists(ins_categories_path):
    with open(ins_categories_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data.get("additives", []):
            ins_categories_db[item["ins"].lower()] = item

with open(ingredients_path, 'r', encoding='utf-8') as f:
    ingredients_db = json.load(f)

docs = []
metadatas = []
ids = []

print("Processing Additives...")
for key, entry in additives_db.items():
    if not isinstance(entry, dict): continue
    names = entry.get('name', {})
    en_name = names.get('en', '')
    if not en_name: continue
    
    clean_name = re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', en_name, flags=re.IGNORECASE)
    
    code = key.replace('en:e', '').lower()
    ins_cat = ins_categories_db.get(code, {})
    
    # Categories
    raw_categories = [k for k, v in entry.items() if isinstance(v, dict) and v.get("en") == "yes" and k not in ["vegan", "vegetarian", "anses_additives_of_interest"]]
    clean_categories = [c.replace('_', ' ').title() for c in raw_categories]
    custom_classes = [c.title() for c in ins_cat.get("functional_class", [])]
    combined_categories = list(set(clean_categories + custom_classes))
    category_str = ", ".join(combined_categories) if combined_categories else "Additive"
    
    # Source
    source = "Unknown"
    if ins_cat and "source" in ins_cat and "category" in ins_cat["source"]:
        raw_cat = ins_cat["source"]["category"]
        if raw_cat == "natural": source = "Natural"
        elif raw_cat == "natural_derived": source = "Natural Derived"
        elif raw_cat == "synthetic/processed": source = "Synthetic / Processed"
    else:
        natural_additives = ['100', '101', '140', '141', '150a', '160a', '160c', '162', '163', '260', '270', '290', '296', '300', '306', '322', '330', '406', '407', '410', '412', '414', '415', '440', '901', '903', '960']
        stripped_code = re.sub(r'[^0-9a-z]', '', code)
        source = "Natural Derived" if stripped_code in natural_additives else "Synthetic / Processed"

    # Risk
    risk_raw = entry.get("efsa_evaluation_overexposure_risk", {}).get("en", "").replace("en:", "")
    if risk_raw == "high": risk = "High Risk"
    elif risk_raw == "moderate": risk = "Moderate Risk"
    elif risk_raw == "low" or risk_raw == "no": risk = "Safe"
    else: risk = "Permitted Additive"
    
    description = entry.get("description", {}).get("en", "") or ins_cat.get("source", {}).get("description", "")
    
    synonyms = list(set([val.lower() for lang, val in names.items()]))
    
    doc_text = f"{clean_name}. {', '.join(synonyms)}. INS {code.upper()}, E{code.upper()}."
    
    docs.append(doc_text)
    metadatas.append({
        "name": clean_name.title(),
        "ins_code": code.upper(),
        "category": category_str,
        "source": source,
        "risk_level": risk,
        "explanation": description,
        "is_additive": True
    })
    ids.append(f"additive_{code}")

print(f"Adding {len(docs)} additives to ChromaDB...")
# Add in batches
batch_size = 500
for i in range(0, len(docs), batch_size):
    collection.add(
        documents=docs[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size],
        ids=ids[i:i+batch_size]
    )
    print(f"Inserted batch {i//batch_size + 1}")

docs = []
metadatas = []
ids = []

print("Processing Standard Ingredients...")
for key, entry in ingredients_db.items():
    if not isinstance(entry, dict): continue
    
    names = entry.get('name', {})
    en_name = names.get('en', '')
    if not en_name: continue
    
    synonyms = list(set([val.lower() for lang, val in names.items()]))
    parents = entry.get("parents", [])
    category_str = ", ".join([p.replace('en:', '').replace('-', ' ').title() for p in parents]) if parents else "Standard Ingredient"
    
    description = entry.get("description", {}).get("en", "")
    
    doc_text = f"{en_name}. {', '.join(synonyms)}."
    
    docs.append(doc_text)
    metadatas.append({
        "name": en_name.title(),
        "ins_code": "",
        "category": category_str,
        "source": "Natural",
        "risk_level": "Safe",
        "explanation": description,
        "is_additive": False
    })
    ids.append(f"ingredient_{key.replace(':', '_')}")

print(f"Adding {len(docs)} standard ingredients to ChromaDB...")
for i in range(0, len(docs), batch_size):
    collection.add(
        documents=docs[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size],
        ids=ids[i:i+batch_size]
    )
    print(f"Inserted batch {i//batch_size + 1}")

print("Successfully built Vector DB!")
