from google.cloud import bigquery
from google.oauth2 import service_account
from core.models.product import ExtractedProductData, NutritionInfo, NutritionFact

class BigQueryService:
    """
    Service to interact with the Ground Truth Dataset (Feature 5 & 10).
    Replaces unreliable OCR data with scientifically verified lab data from the cloud.
    """
    def __init__(self):
        # Authenticate using the Service Account injected by the user
        self.creds = service_account.Credentials.from_service_account_file('gcp-credentials.json')
        self.client = bigquery.Client(credentials=self.creds, project=self.creds.project_id)
        self.table_id = f"{self.creds.project_id}.food_intelligence.canonical_products"

    def enrich_product_data(self, product: ExtractedProductData) -> ExtractedProductData:
        """
        Takes an AI-extracted product, searches BigQuery for a verified match,
        and overrides the AI's guesses with hard scientific data.
        """
        # We search by name or brand to see if we have this product in our verified database
        query = f"""
            SELECT *
            FROM `{self.table_id}`
            WHERE LOWER(name) LIKE @search_term
            OR LOWER(brand) LIKE @search_term
            LIMIT 1
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("search_term", "STRING", f"%{product.name.lower()}%"),
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            
            # Helper to create Pydantic NutritionFact from BigQuery floats
            def make_fact(amount, unit):
                return NutritionFact(amount=float(amount), unit=unit) if amount is not None else None

            # 1. Override the AI's blurry text reading with Verified DB Ingredients
            product.ingredients = list(row.get("ingredients", product.ingredients))
            
            # 2. Override the Nutrition Table with scientific IFCT/Open Food Facts data
            product.nutrition = NutritionInfo(
                calories=make_fact(row.get("calories_kcal"), "kcal") or product.nutrition.calories,
                protein=make_fact(row.get("protein_g"), "g") or product.nutrition.protein,
                carbohydrates=make_fact(row.get("carbs_g"), "g") or product.nutrition.carbohydrates,
                added_sugar=make_fact(row.get("added_sugar_g"), "g") or product.nutrition.added_sugar,
                fiber=make_fact(row.get("fiber_g"), "g") or product.nutrition.fiber,
                sodium=make_fact(row.get("sodium_mg"), "mg") or product.nutrition.sodium,
                saturated_fat=make_fact(row.get("sat_fat_g"), "g") or product.nutrition.saturated_fat,
            )
            
            # 3. Add a verified tag so the frontend knows this is scientifically grounded
            product.claims.append("✅ Verified by BigQuery Ground Truth Database")
            
        return product
