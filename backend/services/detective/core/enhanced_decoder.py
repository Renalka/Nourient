import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from .ins_decoder import IngredientDecoder

class EnhancedIngredientDecoder:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(base_dir, '..', '..', '..', 'data', 'chroma_db')
        
        # Fast standard dictionary lookup
        self.standard_decoder = IngredientDecoder()
        
        # Semantic vector fallback
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_collection("ingredients", embedding_function=self.emb_fn)

    def decode_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 1. Run the highly accurate, regex-aware standard decoder first!
        standard_results = self.standard_decoder.decode_ingredients(ingredients)
        
        final_results = []
        
        # 2. Iterate and patch any failures using the Vector Database
        for idx, item in enumerate(standard_results):
            # If standard decoder successfully categorized it, keep it and move on!
            if item.get("category") != "Uncategorized" or item.get("source") != "Unknown":
                item["vector_match"] = False
                final_results.append(item)
                continue
                
            # If it failed, try the AI Vector DB fallback
            original_text = item.get("original_text", "")
            code_raw = item.get("code", "")
            
            query_text = original_text
            if code_raw:
                query_text = f"{original_text} {code_raw}"
                
            results = self.collection.query(
                query_texts=[query_text],
                n_results=1
            )
            
            best_match = None
            if results and results["distances"] and len(results["distances"][0]) > 0:
                distance = results["distances"][0][0]
                if distance < 0.25:  # Strict threshold
                    best_match = results["metadatas"][0][0]

            if best_match:
                # Patch the standard result with the vector match!
                item["code"] = f"INS {best_match.get('ins_code')}" if best_match.get('ins_code') else None
                item["name"] = best_match.get("name", original_text)
                item["category"] = best_match.get("category", "Uncategorized")
                item["source"] = best_match.get("source", "Unknown")
                item["risk_level"] = best_match.get("risk_level", "Unknown")
                item["explanation"] = best_match.get("explanation", "")
                item["vector_match"] = True
                item["distance"] = float(distance)
            else:
                item["vector_match"] = False
                
            final_results.append(item)

        return final_results
