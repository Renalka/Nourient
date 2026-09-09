import os
import json
import chromadb
from chromadb.utils import embedding_functions

def main():
    print("Starting Claims ETL Pipeline...")
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, '..', 'data')
    json_path = os.path.join(data_dir, 'claims_rules.json')
    db_path = os.path.join(data_dir, 'claims_db')

    if not os.path.exists(json_path):
        print(f"Error: Could not find {json_path}")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Connect to Persistent Vector DB
    print(f"Connecting to Persistent ChromaDB at {db_path}...")
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # 2. Get or Create Collections
    patterns_coll = client.get_or_create_collection("claims_patterns", embedding_function=emb_fn)
    buzzwords_coll = client.get_or_create_collection("buzzwords", embedding_function=emb_fn)

    # 3. Process Patterns
    print(f"Ingesting {len(data['patterns'])} claims patterns...")
    for p in data['patterns']:
        patterns_coll.upsert(
            ids=[p["id"]],
            documents=[p["text"]],
            metadatas=[{
                "type": p["type"],
                "targets": p["targets"],
                "explanation": p["explanation"]
            }]
        )

    # 4. Process Buzzwords
    print(f"Ingesting {len(data['buzzwords'])} buzzwords...")
    for b in data['buzzwords']:
        buzzwords_coll.upsert(
            ids=[b["id"]],
            documents=[b["text"]],
            metadatas=[{
                "score": b["score"],
                "explanation": b["explanation"]
            }]
        )

    print("ETL Pipeline completed successfully! The database is now ready for read-only access.")

if __name__ == "__main__":
    main()
