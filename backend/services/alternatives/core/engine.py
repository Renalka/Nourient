import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AlternativesEngine:
    def __init__(self):
        # We use Open Food Facts instead of BigQuery to remain 100% free
        self.api_url = "https://world.openfoodfacts.org/cgi/search.pl"
        self.headers = {'User-Agent': 'NourientApp/1.0 - Python'}

    def find_better_alternatives(self, category: str, current_sugar: float, current_protein: float, current_price: float) -> List[Dict[str, Any]]:
        """
        Finds alternatives in the same category that are generally healthier using Open Food Facts.
        Prioritizes lower sugar and higher protein.
        """
        if not category:
            return []

        # Standardize category for search
        category_clean = category.lower().strip()
        if not category_clean:
            category_clean = "snack"

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
            'page_size': '10'
        }
        
        results = []
        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            for p in data.get('products', []):
                nutriments = p.get('nutriments', {})
                sugar_g = float(nutriments.get('sugars_100g', 0) or 0)
                protein_g = float(nutriments.get('proteins_100g', 0) or 0)
                
                # Check if it's actually better
                if sugar_g < current_sugar or protein_g > current_protein:
                    sugar_delta = sugar_g - current_sugar
                    protein_delta = protein_g - current_protein
                    
                    deltas = []
                    if sugar_delta < 0:
                        deltas.append(f"{abs(round(sugar_delta, 1))}g less sugar")
                    if protein_delta > 0:
                        deltas.append(f"{round(protein_delta, 1)}g more protein")
                        
                    if not deltas:
                        deltas.append("Healthier overall profile")

                    grade = p.get('nutriscore_grade', 'c').lower()
                    overall_score = 95 if grade == 'a' else 80 if grade == 'b' else 65 if grade == 'c' else 50
                    
                    name = p.get('product_name', '')
                    if not name:
                        continue

                    results.append({
                        "product_id": str(p.get('_id', '')),
                        "name": name,
                        "brand": p.get('brands', 'Unknown Brand'),
                        "price_inr": 0, # OFF doesn't reliably track live prices
                        "sugar_g": sugar_g,
                        "protein_g": protein_g,
                        "overall_score": overall_score,
                        "protein_per_rupee": 0,
                        "improvements": deltas
                    })
                    
                    if len(results) >= 3:
                        break
        except Exception as e:
            logger.error(f"OFF API Error: {e}")
            
        return results
