from google.cloud import bigquery
from google.oauth2 import service_account
from typing import List, Dict, Any

class AlternativesEngine:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file('gcp-credentials.json')
        self.client = bigquery.Client(credentials=self.creds, project="nourient")
        self.table_id = "nourient.food_intelligence.canonical_products"

    def find_better_alternatives(self, category: str, current_sugar: float, current_protein: float, current_price: float) -> List[Dict[str, Any]]:
        """
        Finds alternatives in the same category that are generally healthier.
        Prioritizes lower sugar and higher protein.
        """
        if not category:
            return []

        # Find products in the same category with less sugar or more protein
        # Order by a blended "better" score (lower sugar is good, higher protein is good, lower price is good)
        query = f"""
        SELECT 
            product_id, name, brand, price_inr, sugar_g, protein_g, sodium_mg, overall_score,
            (protein_g / NULLIF(price_inr, 0)) as protein_per_rupee
        FROM `{self.table_id}`
        WHERE category = @category 
          AND (sugar_g < @current_sugar OR protein_g > @current_protein OR overall_score > 50)
        ORDER BY overall_score DESC, protein_g DESC, sugar_g ASC
        LIMIT 3
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("category", "STRING", category),
                bigquery.ScalarQueryParameter("current_sugar", "FLOAT", current_sugar),
                bigquery.ScalarQueryParameter("current_protein", "FLOAT", current_protein)
            ]
        )
        
        results = []
        try:
            rows = self.client.query(query, job_config=job_config).result()
            for row in rows:
                # Calculate Deltas
                sugar_delta = row.sugar_g - current_sugar
                protein_delta = row.protein_g - current_protein
                price_delta = row.price_inr - current_price
                
                deltas = []
                if sugar_delta < 0:
                    deltas.append(f"{abs(sugar_delta)}g less sugar")
                if protein_delta > 0:
                    deltas.append(f"{protein_delta}g more protein")
                if price_delta < 0:
                    deltas.append(f"₹{abs(price_delta)} cheaper")
                    
                if not deltas:
                    deltas.append("Higher overall health score")

                results.append({
                    "product_id": row.product_id,
                    "name": row.name,
                    "brand": row.brand,
                    "price_inr": row.price_inr,
                    "sugar_g": row.sugar_g,
                    "protein_g": row.protein_g,
                    "overall_score": row.overall_score,
                    "protein_per_rupee": round(row.protein_per_rupee, 2) if row.protein_per_rupee else 0,
                    "improvements": deltas
                })
        except Exception as e:
            print(f"BigQuery Error: {e}")
            
        return results
