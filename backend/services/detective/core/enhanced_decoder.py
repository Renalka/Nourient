import os
from pinecone import Pinecone
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from .ins_decoder import IngredientDecoder

class EnhancedIngredientDecoder:
    def __init__(self):
        # Fast standard dictionary lookup
        self.standard_decoder = IngredientDecoder()
        
        # Read-only connection to Pinecone
        self.pc_api_key = os.environ.get("PINECONE_API_KEY")
        if self.pc_api_key:
            self.pc = Pinecone(api_key=self.pc_api_key)
            self.index = self.pc.Index("patchamomma-ingredients")
        else:
            self.index = None
            print("CRITICAL WARNING: PINECONE_API_KEY not set. Enhanced Ingredient Decoder will fail.")
            
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

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
            if not self.index:
                item["vector_match"] = False
                final_results.append(item)
                continue
                
            original_text = item.get("original_text", "")
            code_raw = item.get("code", "")
            
            query_text = original_text
            if code_raw:
                query_text = f"{original_text} {code_raw}"
                
            query_emb = self.emb_fn([query_text])[0]
            if hasattr(query_emb, 'tolist'):
                query_emb = query_emb.tolist()
                
            res = self.index.query(
                vector=query_emb,
                top_k=1,
                include_metadata=True
            )
            
            best_match = None
            distance = 0.0
            if res.matches and len(res.matches) > 0:
                # Pinecone returns similarity score. Higher is better (up to 1.0)
                # We used < 0.25 in Chroma (L2 or Cosine distance), so > 0.75 in Pinecone score
                score = res.matches[0].score
                if score > 0.75:
                    best_match = res.matches[0].metadata
                    # convert similarity score to a "distance" for UI backwards compatibility
                    distance = 1.0 - score

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
