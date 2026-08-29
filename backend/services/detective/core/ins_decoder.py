import json
import re
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class IngredientDecoder:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.additives_path = os.path.join(base_dir, '..', 'data', 'additives.json')
        self.ingredients_path = os.path.join(base_dir, '..', 'data', 'ingredients.json')
        
        self.additives_db = {}
        self.ingredients_db = {}
        self.load_databases()

    def load_databases(self):
        try:
            with open(self.additives_path, 'r', encoding='utf-8') as f:
                self.additives_db = json.load(f)
            logger.info(f"Loaded {len(self.additives_db)} additive records.")
            
            with open(self.ingredients_path, 'r', encoding='utf-8') as f:
                self.ingredients_db = json.load(f)
            logger.info(f"Loaded {len(self.ingredients_db)} standard ingredient records.")
        except Exception as e:
            logger.error(f"Failed to load OFF databases: {e}")

    def decode_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        decoded_results = []
        
        for ingredient in ingredients:
            code_raw = ingredient.get("ins_code")
            name = ingredient.get("name", "")
            
            if not name and not code_raw:
                continue

            # 1. ADDITIVE LOOKUP (if INS code exists)
            if code_raw:
                match = re.search(r'(\d{3,4}[a-z]?)', str(code_raw), re.IGNORECASE)
                if match:
                    code = match.group(1).lower()
                    lookup_key = f"en:e{code}"
                    
                    if lookup_key in self.additives_db:
                        entry = self.additives_db[lookup_key]
                        
                        categories = [k.capitalize() for k, v in entry.items() if isinstance(v, dict) and v.get("en") == "yes" and k not in ["vegan", "vegetarian"]]
                        category_str = ", ".join(categories) if categories else "Additive"
                        
                        raw_name = entry.get("name", {}).get("en", f"Additive {code.upper()}")
                        clean_name = re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', raw_name, flags=re.IGNORECASE)

                        is_vegan = entry.get("vegan", {}).get("en")
                        source = "Plant-Based / Synthetic" if is_vegan == "yes" else "Animal-Derived" if is_vegan == "no" else "Unknown Source"
                        risk = entry.get("efsa_evaluation_safety_assessment", {}).get("en", "Unknown")

                        decoded_results.append({
                            "original_text": name,
                            "percentage": ingredient.get("percentage"),
                            "code": f"INS {code.upper()}",
                            "name": clean_name,
                            "category": category_str,
                            "source": source,
                            "risk_level": risk,
                            "explanation": f"{clean_name} is commonly used as a {category_str.lower()}."
                        })
                        continue

            # 2. STANDARD INGREDIENT LOOKUP
            if name:
                # Convert "Wheat Flour" to "en:wheat-flour"
                normalized_name = re.sub(r'[^a-z0-9]+', '-', name.lower().strip())
                lookup_key = f"en:{normalized_name}"
                
                # Sometimes ingredients are nested under languages or slight variations
                entry = self.ingredients_db.get(lookup_key)
                
                if entry:
                    clean_name = entry.get("name", {}).get("en", name)
                    
                    parents = entry.get("parents", [])
                    category_str = ", ".join([p.replace('en:', '').replace('-', ' ').title() for p in parents]) if parents else "Standard Ingredient"
                    
                    is_vegan = entry.get("vegan", {}).get("en")
                    source = "Plant-Based / Natural" if is_vegan == "yes" else "Animal-Derived" if is_vegan == "no" else "Natural Source"

                    decoded_results.append({
                        "original_text": name,
                        "percentage": ingredient.get("percentage"),
                        "code": None,
                        "name": clean_name.title(),
                        "category": category_str,
                        "source": source,
                        "risk_level": "Safe", # Standard ingredients are generally safe unless flagged by BQ
                        "explanation": f"{clean_name.title()} is a {category_str.lower()}."
                    })
                else:
                    # Fallback for unrecognized ingredients
                    decoded_results.append({
                        "original_text": name,
                        "percentage": ingredient.get("percentage"),
                        "code": None,
                        "name": name.title(),
                        "category": "Uncategorized",
                        "source": "Unknown",
                        "risk_level": "Unknown",
                        "explanation": "This ingredient is not mapped in the local database."
                    })

        return decoded_results
