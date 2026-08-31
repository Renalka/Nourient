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
        self.ins_categories_path = os.path.join(base_dir, '..', '..', '..', 'data', 'ins_food_additives.json')
        
        self.additives_db = {}
        self.ingredients_db = {}
        self.ins_categories_db = {}
        self.synonym_index = {}
        self.load_databases()

    def load_databases(self):
        try:
            with open(self.additives_path, 'r', encoding='utf-8') as f:
                self.additives_db = json.load(f)
            logger.info(f"Loaded {len(self.additives_db)} additive records.")
            
            if os.path.exists(self.ins_categories_path):
                with open(self.ins_categories_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Create a quick lookup dict by INS code (e.g. "100" -> category)
                    for item in data.get("additives", []):
                        self.ins_categories_db[item["ins"].lower()] = item
                logger.info(f"Loaded {len(self.ins_categories_db)} custom INS category records.")
            
            with open(self.ingredients_path, 'r', encoding='utf-8') as f:
                self.ingredients_db = json.load(f)
            
            # Build synonym index for robust standard ingredient lookup
            for key, entry in self.ingredients_db.items():
                if not isinstance(entry, dict):
                    continue
                # Add the primary key (e.g. en:wheat-flour -> wheat-flour)
                clean_key = key.replace('en:', '').replace('-', ' ')
                self.synonym_index[clean_key.lower()] = key
                
                # Add the english name/synonyms
                names = entry.get('name', {})
                if isinstance(names, dict):
                    for lang, val in names.items():
                        self.synonym_index[val.lower().strip()] = key
            
            # ALSO build synonym index for additives! This fixes the bug where "ascorbic acid" falls back to word stripping because it wasn't indexed.
            for key, entry in self.additives_db.items():
                if not isinstance(entry, dict):
                    continue
                names = entry.get('name', {})
                if isinstance(names, dict):
                    for lang, val in names.items():
                        if lang == 'en':
                            clean_val = re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', val, flags=re.IGNORECASE)
                            self.synonym_index[clean_val.lower().strip()] = key
                        
            logger.info(f"Loaded {len(self.ingredients_db)} standard ingredient records with {len(self.synonym_index)} synonyms mapped.")
        except Exception as e:
            logger.error(f"Failed to load OFF databases: {e}")

    def _find_ingredient_key(self, name: str) -> str:
        name = name.lower().strip()
        if not name:
            return None
            
        # 1. Exact match in synonym index
        if name in self.synonym_index:
            return self.synonym_index[name]
            
        # 2. Singular/Plural fallback
        if name.endswith('s') and name[:-1] in self.synonym_index:
            return self.synonym_index[name[:-1]]
        if not name.endswith('s') and f"{name}s" in self.synonym_index:
            return self.synonym_index[f"{name}s"]
            
        # 3. Common Hardcoded Aliases
        aliases = {
            "soy lecithin": "en:soya-lecithin",
            "soyabean": "en:soya-bean",
            "soybean": "en:soya-bean",
            "soybean oil": "en:soya-oil",
            "sodium acid pyrophosphate": "en:e450i",
            "sugar": "en:sugar",
            "salt": "en:salt",
            "water": "en:water",
            "cocoa": "en:cocoa-powder",
            "cocoa powder": "en:cocoa-powder"
        }
        if name in aliases:
            return aliases[name]
            
        # 4. Progressive word stripping from the left
        # Example: "fat reduced cocoa powder" -> "reduced cocoa powder" -> "cocoa powder" -> "powder"
        words = name.split()
        while len(words) > 1:
            words.pop(0)
            reduced_name = " ".join(words)
            if reduced_name in self.synonym_index:
                return self.synonym_index[reduced_name]
            if reduced_name.endswith('s') and reduced_name[:-1] in self.synonym_index:
                return self.synonym_index[reduced_name[:-1]]
                
        # 5. Progressive word stripping from the right
        # Example: "milk chocolate chips" -> "milk chocolate"
        words = name.split()
        while len(words) > 1:
            words.pop(-1)
            reduced_name = " ".join(words)
            if reduced_name in self.synonym_index:
                return self.synonym_index[reduced_name]
                
        return None

    def decode_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        decoded_results = []
        
        for ingredient in ingredients:
            code_raw = ingredient.get("ins_code")
            name = ingredient.get("name", "")
            
            if not name and not code_raw:
                continue

            # First, if there's no code but there is a name, check if the name is actually an additive!
            lookup_key = self._find_ingredient_key(name) if name else None
            
            if not code_raw and lookup_key and lookup_key.startswith("en:e"):
                # The name mapped directly to an additive (e.g. "ascorbic acid" -> "en:e300")
                code_raw = lookup_key.replace("en:e", "")
                
            # 1. ADDITIVE LOOKUP (if INS code exists or was resolved from name)
            if code_raw:
                match = re.search(r'(\d{3,4}[a-z]?)', str(code_raw), re.IGNORECASE)
                if match:
                    code = match.group(1).lower()
                    lookup_key_additive = f"en:e{code}"
                    
                    in_off_db = lookup_key_additive in self.additives_db
                    in_custom_db = code in self.ins_categories_db
                    
                    if in_off_db or in_custom_db:
                        entry = self.additives_db.get(lookup_key_additive, {})
                        custom_entry = self.ins_categories_db.get(code, {})
                        
                        # 1. Parse categories (Second Label)
                        raw_categories = [k for k, v in entry.items() if isinstance(v, dict) and v.get("en") == "yes" and k not in ["vegan", "vegetarian", "anses_additives_of_interest"]]
                        clean_categories = [c.replace('_', ' ').title() for c in raw_categories]
                        
                        custom_classes = [c.title() for c in custom_entry.get("functional_class", [])]
                        combined_categories = list(set(clean_categories + custom_classes))
                        category_str = ", ".join(combined_categories) if combined_categories else "Additive"
                        
                        # 2. Parse name
                        raw_name = entry.get("name", {}).get("en") or custom_entry.get("name") or f"Additive {code.upper()}"
                        clean_name = re.sub(r'^E\d+[a-zA-Z]?\s*-\s*', '', raw_name, flags=re.IGNORECASE)

                        # 3. Parse Source (First Label)
                        if custom_entry and "source" in custom_entry and "category" in custom_entry["source"]:
                            raw_cat = custom_entry["source"]["category"]
                            if raw_cat == "natural":
                                source = "Natural"
                            elif raw_cat == "natural_derived":
                                source = "Natural Derived"
                            elif raw_cat == "synthetic/processed":
                                source = "Synthetic / Processed"
                            else:
                                source = "Unknown"
                        elif in_off_db:
                            # Fallback heuristic if in OFF but not in custom DB
                            natural_additives = ['100', '101', '140', '141', '150a', '160a', '160c', '162', '163', '260', '270', '290', '296', '300', '306', '322', '330', '406', '407', '410', '412', '414', '415', '440', '901', '903', '960']
                            stripped_code = re.sub(r'[^0-9a-z]', '', code)
                            source = "Natural Derived" if stripped_code in natural_additives else "Synthetic / Processed"
                        else:
                            source = "Unknown"
                        
                        # 4. Parse Risk (Third Label)
                        risk_raw = entry.get("efsa_evaluation_overexposure_risk", {}).get("en", "").replace("en:", "")
                        if risk_raw == "high":
                            risk = "High Risk"
                        elif risk_raw == "moderate":
                            risk = "Moderate Risk"
                        elif risk_raw == "low" or risk_raw == "no":
                            risk = "Safe"
                        else:
                            risk = "Permitted Additive"

                        description = entry.get("description", {}).get("en", "") or custom_entry.get("source", {}).get("description", "")

                        # Construct final name showing original and canonical
                        if name and name.lower().strip() != clean_name.lower().strip():
                            final_name = f"{name.title()} ({clean_name.title()})"
                        else:
                            final_name = name.title() if name else clean_name.title()

                        decoded_results.append({
                            "original_text": name,
                            "percentage": ingredient.get("percentage"),
                            "code": f"INS {code.upper()}",
                            "name": final_name,
                            "category": category_str,
                            "source": source,
                            "risk_level": risk,
                            "explanation": description
                        })
                        continue

            # 2. STANDARD INGREDIENT LOOKUP
            if name:
                lookup_key = self._find_ingredient_key(name)
                
                # Sometimes ingredients are nested under languages or slight variations
                entry = self.ingredients_db.get(lookup_key) if lookup_key else None
                
                if entry:
                    clean_name = entry.get("name", {}).get("en", name)
                    
                    parents = entry.get("parents", [])
                    category_str = ", ".join([p.replace('en:', '').replace('-', ' ').title() for p in parents]) if parents else "Standard Ingredient"
                    
                    source = "Natural"
                    description = entry.get("description", {}).get("en", "")

                    if name and name.lower().strip() != clean_name.lower().strip():
                        final_name = f"{name.title()} ({clean_name.title()})"
                    else:
                        final_name = name.title()

                    decoded_results.append({
                        "original_text": name,
                        "percentage": ingredient.get("percentage"),
                        "code": None,
                        "name": final_name,
                        "category": category_str,
                        "source": source,
                        "risk_level": "Safe", # Standard ingredients are generally safe unless flagged by BQ
                        "explanation": description
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
                        "explanation": ""
                    })

        return decoded_results

    def search_ingredients(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Fast in-memory autocomplete search across all databases."""
        query = query.lower().strip()
        if not query or len(query) < 2:
            return []
            
        matched_aliases = []
        # 1. Prefix matches first (e.g. "ascor" -> "ascorbic acid")
        for alias in self.synonym_index.keys():
            if alias.startswith(query):
                matched_aliases.append(alias)
                if len(matched_aliases) >= limit:
                    break
                    
        # 2. Substring matches if we need more (e.g. "pyrophos" -> "sodium acid pyrophosphate")
        if len(matched_aliases) < limit:
            for alias in self.synonym_index.keys():
                if query in alias and alias not in matched_aliases:
                    matched_aliases.append(alias)
                    if len(matched_aliases) >= limit:
                        break
                        
        # Mock them as ingredients and run them through the core decoder engine!
        fake_ingredients = [{"name": alias} for alias in matched_aliases]
        
        # 3. INS Code matching (e.g. user types "300", "e300", "ins 30")
        clean_q = query.replace("e", "").replace("ins", "").replace(" ", "").strip()
        if clean_q and clean_q.isalnum() and clean_q[0].isdigit():
            prefix = f"en:e{clean_q}"
            matched_ins = 0
            for k in self.additives_db.keys():
                if k.startswith(prefix):
                    ins_code = k.replace("en:e", "")
                    fake_ingredients.append({"ins_code": ins_code})
                    matched_ins += 1
                    if matched_ins >= 10: # Limit INS matches so we don't overwhelm
                        break
                        
        raw_results = self.decode_ingredients(fake_ingredients)
        
        # Deduplicate and filter out unknowns
        unique_results = []
        seen_names = set()
        
        for r in raw_results:
            if r["category"] == "Uncategorized" and r["source"] == "Unknown":
                continue
                
            # The core decoder outputs things like "Ascorbic Acid (Ascorbic Acid)". Let's clean that up for the dictionary view.
            clean_name = r["name"]
            if "(" in clean_name and clean_name.split("(")[0].strip().lower() == clean_name.split("(")[1].replace(")", "").strip().lower():
                clean_name = clean_name.split("(")[0].strip()
                r["name"] = clean_name
                
            if clean_name.lower() not in seen_names:
                seen_names.add(clean_name.lower())
                unique_results.append(r)
                
        return unique_results
