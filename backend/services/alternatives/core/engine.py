import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def _get_macro(nutriments: dict, key: str) -> Optional[float]:
    val = nutriments.get(key)
    if val in (None, ""):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

class AlternativesEngine:
    def __init__(self):
        self.api_url = "https://world.openfoodfacts.org/cgi/search.pl"
        self.headers = {'User-Agent': 'NourientApp/1.0 - Python'}

    def find_better_alternatives(self, category: str, 
                                 current_sugar: Optional[float] = None, 
                                 current_protein: Optional[float] = None,
                                 current_fat: Optional[float] = None,
                                 current_saturated_fat: Optional[float] = None,
                                 current_fiber: Optional[float] = None,
                                 current_sodium: Optional[float] = None) -> List[Dict[str, Any]]:
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
            'page_size': '40'
        }
        
        results = []
        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=5)
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
                
                sugar_g = _get_macro(nutriments, 'sugars_100g')
                protein_g = _get_macro(nutriments, 'proteins_100g')
                fat_g = _get_macro(nutriments, 'fat_100g')
                sat_fat_g = _get_macro(nutriments, 'saturated-fat_100g')
                fiber_g = _get_macro(nutriments, 'fiber_100g')
                sodium_g = _get_macro(nutriments, 'sodium_100g')
                
                # Missing critical data check
                missing_data = False
                if current_sugar is not None and sugar_g is None: missing_data = True
                if current_protein is not None and protein_g is None: missing_data = True
                if current_fat is not None and fat_g is None: missing_data = True
                if current_saturated_fat is not None and sat_fat_g is None: missing_data = True
                if current_fiber is not None and fiber_g is None: missing_data = True
                if current_sodium is not None and sodium_g is None: missing_data = True
                
                if missing_data:
                    continue
                
                is_better = False
                if current_sugar is not None and sugar_g < current_sugar: is_better = True
                if current_protein is not None and protein_g > current_protein: is_better = True
                if current_fat is not None and fat_g < current_fat: is_better = True
                if current_saturated_fat is not None and sat_fat_g < current_saturated_fat: is_better = True
                if current_fiber is not None and fiber_g > current_fiber: is_better = True
                if current_sodium is not None and sodium_g < current_sodium: is_better = True
                
                if not is_better:
                    continue
                    
                betterment_score = random.uniform(0.0, 1.0)
                deltas = []
                
                if current_sugar is not None:
                    if current_sugar <= 10.0 and sugar_g > (current_sugar * 1.5): continue
                    improvement = max(0, current_sugar - sugar_g)
                    betterment_score += improvement * 2.5
                    if improvement > 0.5: deltas.append(f"{round(improvement, 1)}g less sugar")

                if current_protein is not None:
                    if current_protein >= 5.0 and protein_g < (current_protein * 0.7): continue
                    improvement = max(0, protein_g - current_protein)
                    betterment_score += improvement * 3.0
                    if improvement > 0.5: deltas.append(f"{round(improvement, 1)}g more protein")
                    
                if current_fat is not None:
                    if current_fat <= 10.0 and fat_g > (current_fat * 1.5): continue
                    improvement = max(0, current_fat - fat_g)
                    betterment_score += improvement * 1.5
                    if improvement > 0.5: deltas.append(f"{round(improvement, 1)}g less fat")

                if current_saturated_fat is not None:
                    if current_saturated_fat <= 5.0 and sat_fat_g > (current_saturated_fat * 1.5): continue
                    improvement = max(0, current_saturated_fat - sat_fat_g)
                    betterment_score += improvement * 2.0
                    if improvement > 0.5: deltas.append(f"{round(improvement, 1)}g less sat fat")

                if current_fiber is not None:
                    if current_fiber >= 3.0 and fiber_g < (current_fiber * 0.7): continue
                    improvement = max(0, fiber_g - current_fiber)
                    betterment_score += improvement * 2.5
                    if improvement > 0.5: deltas.append(f"{round(improvement, 1)}g more fiber")

                if current_sodium is not None:
                    if current_sodium <= 0.5 and sodium_g > (current_sodium * 1.5): continue
                    improvement = max(0, current_sodium - sodium_g)
                    betterment_score += improvement * 10.0
                    if improvement > 0.05: deltas.append(f"{round(improvement, 2)}g less sodium")

                if not deltas:
                    deltas.append("Healthier overall profile")

                grade = p.get('nutriscore_grade', 'c').lower()
                overall_score = 95 if grade == 'a' else 80 if grade == 'b' else 65 if grade == 'c' else 50
                betterment_score += overall_score
                
                candidates.append({
                    "product_id": str(p.get('_id', '')),
                    "name": name,
                    "brand": p.get('brands', 'Unknown Brand'),
                    "nutriscore_grade": grade.upper(),
                    "overall_score": overall_score,
                    "betterment_score": int(betterment_score),
                    "improvements": deltas,
                    "sugar_g": sugar_g,
                    "protein_g": protein_g,
                    "fat_g": fat_g,
                    "sat_fat_g": sat_fat_g,
                    "fiber_g": fiber_g,
                    "sodium_g": sodium_g
                })

            candidates.sort(key=lambda x: x["betterment_score"], reverse=True)
            results = candidates[:10]
            
        except Exception as e:
            logger.error(f"OFF API Error: {e}")
            
        return results
