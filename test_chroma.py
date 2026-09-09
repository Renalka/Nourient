from chromadb.utils import embedding_functions
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
emb1 = emb_fn(["no artificial flavors and colors"])[0]
emb2 = emb_fn(["No Artificial Flavors or Colors"])[0]
import numpy as np
# chroma uses l2 distance by default. 
dist = np.linalg.norm(np.array(emb1) - np.array(emb2)) ** 2
print("Distance:", dist)
