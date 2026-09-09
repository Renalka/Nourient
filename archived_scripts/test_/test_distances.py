import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="data/chroma_db")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_collection("ingredients", embedding_function=emb_fn)

queries = ["Enriched unbleached flour", "honey powder", "Citric Acid", "Salt"]
results = collection.query(query_texts=queries, n_results=3)

for i, q in enumerate(queries):
    print(f"Query: {q}")
    for j in range(len(results['distances'][i])):
        dist = results['distances'][i][j]
        meta = results['metadatas'][i][j]
        print(f"  - {meta['name']} (Dist: {dist:.3f})")
