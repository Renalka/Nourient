import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from core.models.product import FrontOfPackData, ExtractedProductData

class ClaimsEngine:
    def __init__(self):
        # We will use an in-memory ephemeral client for speed during this session
        # and seed it with known contradiction patterns and loopholes.
        self.client = chromadb.EphemeralClient()
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        self.patterns_coll = self.client.create_collection("claims_patterns", embedding_function=self.emb_fn)
        self.buzzwords_coll = self.client.create_collection("buzzwords", embedding_function=self.emb_fn)
        
        self._seed_db()

    def _seed_db(self):
        # 1. Contradictions & Loopholes
        patterns = [
            {
                "id": "p1",
                "text": "No Artificial Sweeteners",
                "meta": {"type": "contradiction", "targets": "sucralose, aspartame, acesulfame potassium, saccharin, neotame", "explanation": "Found artificial sweeteners despite 'No Artificial Sweeteners' claim."}
            },
            {
                "id": "p2",
                "text": "Plant-Based or Vegan",
                "meta": {"type": "contradiction", "targets": "carmine, gelatin, milk, whey, casein, honey, beeswax, shellac", "explanation": "Found animal-derived ingredients despite 'Plant-Based' or 'Vegan' claim."}
            },
            {
                "id": "p3",
                "text": "No Added Nitrates or Nitrites",
                "meta": {"type": "loophole", "targets": "celery powder, celery juice, celery extract", "explanation": "Uses celery powder, which naturally contains high nitrates that chemically convert to nitrites in your body."}
            },
            {
                "id": "p4",
                "text": "Zero Sugar or Sugar Free",
                "meta": {"type": "loophole", "targets": "", "explanation": "Legal loophole: 'Zero Sugar' means less than 0.5g of sugar per serving. If you eat the whole package, you are still consuming sugar."}
            },
            {
                "id": "p5",
                "text": "No Preservatives",
                "meta": {"type": "contradiction", "targets": "sodium benzoate, potassium sorbate, calcium propionate, bht, bha, tbhq, edta", "explanation": "Found chemical preservatives despite 'No Preservatives' claim."}
            },
            {
                "id": "p6",
                "text": "Made with Real Fruit",
                "meta": {"type": "loophole", "targets": "fruit juice concentrate, fruit puree", "explanation": "'Real fruit' is often just a highly processed fruit juice concentrate stripped of fiber and behaving identically to added sugar."}
            },
            {
                "id": "p7",
                "text": "No Artificial Flavors",
                "meta": {"type": "contradiction", "targets": "artificial flavor, synthetic flavor, flavor enhancer, flavour enhancer, msg, monosodium glutamate, disodium inosinate, disodium guanylate, ins 627, ins 631, ins 621", "explanation": "Found synthetic flavor enhancers despite 'No Artificial Flavors' claim."}
            },
            {
                "id": "p8",
                "text": "No Artificial Colors",
                "meta": {"type": "contradiction", "targets": "red 40, yellow 5, yellow 6, blue 1, blue 2, green 3, artificial color, synthetic color, caramel color", "explanation": "Found artificial food dyes despite 'No Artificial Colors' claim."}
            },
            {
                "id": "p9",
                "text": "No Artificial Flavors or Colors",
                "meta": {"type": "contradiction", "targets": "artificial flavor, synthetic flavor, flavor enhancer, flavour enhancer, msg, monosodium glutamate, disodium inosinate, disodium guanylate, ins 627, ins 631, ins 621, red 40, yellow 5, yellow 6, blue 1, blue 2, green 3, artificial color, synthetic color, caramel color", "explanation": "Found synthetic flavor enhancers or artificial food dyes despite the 'No Artificial Flavors or Colors' claim."}
            }
        ]
        
        self.patterns_coll.add(
            ids=[p["id"] for p in patterns],
            documents=[p["text"] for p in patterns],
            metadatas=[p["meta"] for p in patterns]
        )

        # 2. Buzzwords
        buzzwords = [
            {"id": "b1", "text": "Superfood", "meta": {"score": 90, "explanation": "An unregulated marketing term designed to inflate perceived health benefits."}},
            {"id": "b2", "text": "Detox", "meta": {"score": 100, "explanation": "A medically meaningless term. Your liver and kidneys handle detoxing."}},
            {"id": "b3", "text": "Artisan or Handcrafted", "meta": {"score": 70, "explanation": "Often used on mass-produced items to justify a premium price markup."}},
            {"id": "b4", "text": "All Natural", "meta": {"score": 85, "explanation": "Highly unregulated by the FDA. Can still contain heavily processed ingredients."}},
            {"id": "b5", "text": "Guilt-Free", "meta": {"score": 95, "explanation": "An emotional manipulation tactic to encourage overconsumption."}}
        ]
        
        self.buzzwords_coll.add(
            ids=[b["id"] for b in buzzwords],
            documents=[b["text"] for b in buzzwords],
            metadatas=[b["meta"] for b in buzzwords]
        )

    def verify(self, claims: List[str], ingredients_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        contradictions = []
        loopholes = []
        buzzwords = []
        
        ingredient_names = [ing.get("name", "").lower() for ing in ingredients_data]

        for claim in claims:
            # 1. Check Buzzwords
            b_results = self.buzzwords_coll.query(query_texts=[claim], n_results=1)
            if b_results["distances"] and len(b_results["distances"][0]) > 0 and b_results["distances"][0][0] < 0.6:
                meta = b_results["metadatas"][0][0]
                buzzwords.append({
                    "word": claim,
                    "fluff_score": meta["score"],
                    "explanation": meta["explanation"]
                })
                
            # 2. Check Patterns
            p_results = self.patterns_coll.query(query_texts=[claim], n_results=1)
            if p_results["distances"] and len(p_results["distances"][0]) > 0 and p_results["distances"][0][0] < 0.6:
                meta = p_results["metadatas"][0][0]
                ptype = meta["type"]
                targets = [t.strip() for t in meta["targets"].split(",") if t.strip()]
                
                if ptype == "contradiction":
                    # Check if any target is in the ingredients list
                    found_targets = []
                    for ing in ingredient_names:
                        for t in targets:
                            if t in ing:
                                found_targets.append(ing.title())
                    
                    if found_targets:
                        contradictions.append({
                            "claim": claim,
                            "contradicting_ingredient": ", ".join(list(set(found_targets))),
                            "explanation": meta["explanation"]
                        })
                
                elif ptype == "loophole":
                    # For loopholes with targets (like celery powder), check ingredients
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
                                "reality_check": meta["explanation"]
                            })
                    else:
                        # Unconditional loophole (e.g. Zero Sugar)
                        loopholes.append({
                            "claim": claim,
                            "true_meaning": "Regulatory Definition",
                            "reality_check": meta["explanation"]
                        })

        # Calculate overall trust score
        penalty = (len(contradictions) * 30) + (len(loopholes) * 15) + sum([b["fluff_score"]/10 for b in buzzwords])
        trust_score = max(0, min(100, 100 - penalty))

        return {
            "contradictions": contradictions,
            "loopholes": loopholes,
            "buzzwords": buzzwords,
            "overall_trust_score": int(trust_score)
        }
