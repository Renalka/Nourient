import os
from dotenv import load_dotenv
load_dotenv()
import json
from pinecone import Pinecone, ServerlessSpec
from chromadb.utils import embedding_functions

def main():
    print("Starting Pinecone Claims ETL Pipeline...")
    pc_api_key = os.environ.get("PINECONE_API_KEY")
    
    if not pc_api_key:
        print("CRITICAL ERROR: PINECONE_API_KEY environment variable not set.")
        print("Please export PINECONE_API_KEY='your-key' before running this script.")
        return

    # 1. Connect to Pinecone
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=pc_api_key)
    index_name = "patchamomma-claims"

    # 2. Get or Create Index
    if index_name not in pc.list_indexes().names():
        print(f"Creating Pinecone index '{index_name}' (dimension 384 for MiniLM)...")
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    index = pc.Index(index_name)

    # 3. Load Data
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, '..', 'data', 'claims_rules.json')
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 4. Initialize Local Embedding Function
    print("Initializing embedding model (Downloading if first time)...")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # 5. Process Patterns (Namespace: patterns)
    print(f"Embedding and upserting {len(data['patterns'])} claims patterns to Pinecone...")
    pattern_vectors = []
    for p in data['patterns']:
        vec = emb_fn([p["text"]])[0]
        pattern_vectors.append({
            "id": p["id"],
            "values": vec,
            "metadata": {
                "type": p["type"],
                "targets": p["targets"],
                "explanation": p["explanation"]
            }
        })
    index.upsert(vectors=pattern_vectors, namespace="patterns")

    # 6. Process Buzzwords (Namespace: buzzwords)
    print(f"Embedding and upserting {len(data['buzzwords'])} buzzwords to Pinecone...")
    buzzword_vectors = []
    for b in data['buzzwords']:
        vec = emb_fn([b["text"]])[0]
        buzzword_vectors.append({
            "id": b["id"],
            "values": vec,
            "metadata": {
                "score": b["score"],
                "explanation": b["explanation"]
            }
        })
    index.upsert(vectors=buzzword_vectors, namespace="buzzwords")

    print("✅ ETL Pipeline completed successfully! Your data is now live on Pinecone.")

if __name__ == "__main__":
    main()
