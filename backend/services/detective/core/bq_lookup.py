from google.cloud import bigquery
from google.oauth2 import service_account
from typing import List, Dict

class DetectiveService:
    """
    Ingredient Detective (Feature 7 & 8).
    Queries BigQuery to find complex additives in the ingredient list and returns their scientific risk tier.
    """
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file('gcp-credentials.json')
        self.client = bigquery.Client(credentials=self.creds, project=self.creds.project_id)
        self.table_id = f"{self.creds.project_id}.food_intelligence.ingredient_dictionary"

    def analyze_ingredients(self, ingredients: List[str]) -> List[Dict]:
        if not ingredients:
            return []

        # Convert to lower case for loose matching
        query_str = " OR ".join([f"LOWER(@ing_{i}) LIKE CONCAT('%', LOWER(name), '%')" for i in range(len(ingredients))])
        
        query = f"""
            SELECT *
            FROM `{self.table_id}`
            WHERE {query_str}
        """
        
        query_parameters = [
            bigquery.ScalarQueryParameter(f"ing_{i}", "STRING", ing) for i, ing in enumerate(ingredients)
        ]
        
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        
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
