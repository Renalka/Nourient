import os
from dotenv import load_dotenv
load_dotenv()
from pinecone import Pinecone
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class ClaimsEngine:
    def __init__(self):
        # Read-only connection to Pinecone
        self.pc_api_key = os.environ.get("PINECONE_API_KEY")
        if self.pc_api_key:
            self.pc = Pinecone(api_key=self.pc_api_key)
            self.index = self.pc.Index("patchamomma-claims")
        else:
            self.index = None
            print("CRITICAL WARNING: PINECONE_API_KEY not set. Claims Engine will fail.")
            
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    def verify(self, claims: List[str], ingredients_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.index:
            return {"error": "Pinecone API Key missing", "overall_trust_score": 0}

        contradictions = []
        loopholes = []
        buzzwords = []
        
        ingredient_names = [ing.get("name", "").lower() for ing in ingredients_data]

        for claim in claims:
            # Create the embedding for the query
            query_emb = self.emb_fn([claim])[0]
            if hasattr(query_emb, 'tolist'):
                query_emb = query_emb.tolist()

            # 1. Check Buzzwords (Namespace: buzzwords)
            b_res = self.index.query(
                vector=query_emb,
                top_k=1,
                namespace="buzzwords",
                include_metadata=True
            )
            # Pinecone returns similarity score. For Cosine, 1.0 is identical.
            # A score > 0.6 is a good threshold for "close match" (similar to distance < 0.4 in Chroma)
            if b_res.matches and b_res.matches[0].score > 0.6:
                meta = b_res.matches[0].metadata
                buzzwords.append({
                    "word": claim,
                    "fluff_score": meta.get("score"),
                    "explanation": meta.get("explanation")
                })
                
            # 2. Check Patterns (Namespace: patterns)
            p_res = self.index.query(
                vector=query_emb,
                top_k=1,
                namespace="patterns",
                include_metadata=True
            )
            if p_res.matches and p_res.matches[0].score > 0.6:
                meta = p_res.matches[0].metadata
                ptype = meta.get("type")
                targets = [t.strip() for t in meta.get("targets", "").split(",") if t.strip()]
                
                if ptype == "contradiction":
                    found_targets = []
                    for ing in ingredient_names:
                        for t in targets:
                            if t in ing:
                                found_targets.append(ing.title())
                    
                    if found_targets:
                        contradictions.append({
                            "claim": claim,
                            "contradicting_ingredient": ", ".join(list(set(found_targets))),
                            "explanation": meta.get("explanation")
                        })
                
                elif ptype == "loophole":
                    found_targets = []
                    if targets:
                        for ing in ingredient_names:
                            for t in targets:
                                if t in ing:
                                    found_targets.append(ing.title())
                        
                        if found_targets:
                            loopholes.append({
                                "claim": claim,
                                "true_meaning": f"Found: {', '.join(list(set(found_targets)))}",
                                "reality_check": meta.get("explanation")
                            })
                    else:
                        loopholes.append({
                            "claim": claim,
                            "true_meaning": "Regulatory Definition",
                            "reality_check": meta.get("explanation")
                        })

        penalty = (len(contradictions) * 30) + (len(loopholes) * 15) + sum([b["fluff_score"]/10 for b in buzzwords])
        trust_score = max(0, min(100, 100 - penalty))

        return {
            "contradictions": contradictions,
            "loopholes": loopholes,
            "buzzwords": buzzwords,
            "overall_trust_score": int(trust_score)
        }
