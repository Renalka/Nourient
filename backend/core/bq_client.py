from google.cloud import bigquery
from core.models.product import ExtractedProductData, NutritionInfo, NutritionFact
from core.gcp import source_bigquery_project_id
import os

class BigQueryService:
    """
    Service to interact with the Ground Truth Dataset (Feature 5 & 10).
    Replaces unreliable OCR data with scientifically verified lab data from the cloud.
    """
    def __init__(self):
        # Cloud Run uses Application Default Credentials from its service account.
        # Query jobs run in BQ_BILLING_PROJECT_ID (the trial project) while data
        # remains in BQ_DATA_PROJECT_ID (the existing project).
        billing_project = os.environ.get("BQ_BILLING_PROJECT_ID")
        self.client = bigquery.Client(project=billing_project)
        self.table_id = f"{source_bigquery_project_id()}.food_intelligence.canonical_products"

    def enrich_product_data(self, product: ExtractedProductData) -> ExtractedProductData:
        """
        Takes an AI-extracted product, searches BigQuery for a verified match,
        and overrides the AI's guesses with hard scientific data.
        """
        # We search by name or brand to see if we have this product in our verified database
        query = f"""
            SELECT name, brand, ingredients, calories_kcal, protein_g, carbs_g,
                   added_sugar_g, fiber_g, sodium_mg, sat_fat_g
            FROM `{self.table_id}`
            WHERE LOWER(name) LIKE @search_term
            OR LOWER(brand) LIKE @search_term
            LIMIT 1
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("search_term", "STRING", f"%{product.name.lower()}%"),
            ],
            maximum_bytes_billed=int(os.environ.get("BQ_MAXIMUM_BYTES_BILLED", "50000000")),
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
