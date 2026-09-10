import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AlternativesEngine:
    def __init__(self):
        # We use Open Food Facts instead of BigQuery to remain 100% free
        self.api_url = "https://world.openfoodfacts.org/cgi/search.pl"
        self.headers = {'User-Agent': 'NourientApp/1.0 - Python'}

    def find_better_alternatives(self, category: str, current_sugar: float, current_protein: float) -> List[Dict[str, Any]]:
        """
        Finds healthier alternatives using Open Food Facts.
        Dynamically scores fetched products against the user's specific inputs to ensure diverse recommendations.
        """
        if not category:
            category = "snack"

        category_clean = category.lower().strip()

        # Build initial query
        params = {
            'action': 'process',
            'json': 'true',
            'tagtype_0': 'countries',
            'tag_contains_0': 'contains',
            'tag_0': 'india',
            'tagtype_1': 'categories',
            'tag_contains_1': 'contains',
            'tag_1': category_clean,
            'sort_by': 'nutriscore_score',
            'page_size': '40' # Fetch a large pool to dynamically sort
        }
        
        results = []
        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=5)
            # If the category throws a 503 or 404, fallback to a free-text search for the category in India
            if response.status_code != 200:
                logger.warning(f"OFF API returned {response.status_code} for {category_clean}, falling back to free-text search.")
                del params['tagtype_1']
                del params['tag_contains_1']
                del params['tag_1']
                params['search_terms'] = category_clean
                response = requests.get(self.api_url, params=params, headers=self.headers, timeout=5)
                
            response.raise_for_status()
            data = response.json()
            
            candidates = []
            
            import random
            
            for p in data.get('products', []):
                name = p.get('product_name', '')
                if not name:
                    continue
                    
                nutriments = p.get('nutriments', {})
                
                # STRICT DATA INTEGRITY CHECK: Reject products with missing macros
                # A missing value might just mean the uploader didn't enter it, not that it is 0g.
                raw_sugar = nutriments.get('sugars_100g')
                raw_protein = nutriments.get('proteins_100g')
                
                if raw_sugar in (None, "") or raw_protein in (None, ""):
                    continue
                    
                try:
                    sugar_g = float(raw_sugar)
                    protein_g = float(raw_protein)
                except (ValueError, TypeError):
                    continue
                
                is_better = False
                
                # Protect against bad downgrades if the user wants high protein or low sugar
                if current_protein >= 5.0 and protein_g < (current_protein * 0.7):
                    continue # It's a huge downgrade in protein, skip it!
                if current_sugar <= 10.0 and sugar_g > (current_sugar * 1.5):
                    continue # It's a huge downgrade in sugar, skip it!
                    
                if sugar_g < current_sugar and protein_g >= current_protein:
                    is_better = True # Straight up better in both
                elif sugar_g < current_sugar and current_protein < 5.0:
                    is_better = True # Better sugar, protein doesn't matter much
                elif protein_g > current_protein and current_sugar >= 5.0:
                    is_better = True # Better protein, and we didn't sacrifice a low sugar item
                    
                if is_better:
                    sugar_improvement = max(0, current_sugar - sugar_g)
                    protein_improvement = max(0, protein_g - current_protein)
                    
                    # Weight protein and sugar heavily, add tiny random noise to break ties
                    betterment_score = (sugar_improvement * 2.5) + (protein_improvement * 3.0) + random.uniform(0.0, 1.0)
                    
                    deltas = []
                    if sugar_improvement > 0.5:
                        deltas.append(f"{round(sugar_improvement, 1)}g less sugar")
                    if protein_improvement > 0.5:
                        deltas.append(f"{round(protein_improvement, 1)}g more protein")
                        
                    if not deltas:
                        deltas.append("Healthier overall profile")

                    grade = p.get('nutriscore_grade', 'c').lower()
                    overall_score = 95 if grade == 'a' else 80 if grade == 'b' else 65 if grade == 'c' else 50
                    
                    betterment_score += overall_score
                    
                    candidates.append({
                        "product_id": str(p.get('_id', '')),
                        "name": name,
                        "brand": p.get('brands', 'Unknown Brand'),
                        "price_inr": None,
                        "sugar_g": sugar_g,
                        "protein_g": protein_g,
                        "overall_score": overall_score,
                        "betterment_score": betterment_score,
                        "improvements": deltas
                    })

            # Sort candidates by the custom betterment score descending
            candidates.sort(key=lambda x: x["betterment_score"], reverse=True)
            
            # Return up to 10 most relevant alternatives
            results = candidates[:10]
            
        except Exception as e:
            logger.error(f"OFF API Error: {e}")
            
        return results
