from google.cloud import bigquery
from typing import List, Dict
from core.gcp import source_bigquery_project_id
import os

class DetectiveService:
    """
    Ingredient Detective (Feature 7 & 8).
    Queries BigQuery to find complex additives in the ingredient list and returns their scientific risk tier.
    """
    def __init__(self):
        self.client = bigquery.Client(project=os.environ.get("BQ_BILLING_PROJECT_ID"))
        # Pointing to the real production data loaded via ETL
        self.table_id = f"{source_bigquery_project_id()}.food_intelligence.ingredient_dictionary_real"

    def analyze_ingredients(self, ingredients: List[Dict]) -> List[Dict]:
        if not ingredients:
            return []
            
        # Extract the names from the structured dictionaries
        ingredient_names = [ing.get("name", "") for ing in ingredients if ing.get("name")]

        # Convert to lower case for loose matching
        query_str = " OR ".join([f"LOWER(@ing_{i}) LIKE CONCAT('%', LOWER(name), '%')" for i in range(len(ingredient_names))])
        
        query = f"""
            SELECT name, purpose, confidence_tier, explanation
            FROM `{self.table_id}`
            WHERE {query_str}
        """
        
        query_parameters = [
            bigquery.ScalarQueryParameter(f"ing_{i}", "STRING", ing) for i, ing in enumerate(ingredient_names)
        ]
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=query_parameters,
            maximum_bytes_billed=int(os.environ.get("BQ_MAXIMUM_BYTES_BILLED", "50000000")),
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job.result())
            
            flagged = []
            for row in results:
                flagged.append({
                    "name": row.get("name"),
                    "purpose": row.get("purpose"),
                    "confidence_tier": row.get("confidence_tier"),
                    "explanation": row.get("explanation")
                })
            return flagged
        except Exception as e:
            print(f"Detective DB Error: {e}")
            return []
