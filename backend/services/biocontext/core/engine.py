from google.cloud import bigquery
from google.oauth2 import service_account
from pydantic import BaseModel
from typing import Dict, Any

class BioContextResult(BaseModel):
    user_name: str
    health_profile: str
    metabolic_fit_score: int
    context_reasoning: str

class BioContextEngine:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file('gcp-credentials.json')
        self.client = bigquery.Client(credentials=self.creds, project=self.creds.project_id)
        self.table_id = f"{self.creds.project_id}.food_intelligence.users"

    def fetch_user(self, user_id: str) -> Dict[str, str]:
        query = f"SELECT name, health_profile FROM `{self.table_id}` WHERE user_id = @user_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
        )
        results = list(self.client.query(query, job_config=job_config).result())
        if results:
            return {"name": results[0].name, "health_profile": results[0].health_profile}
        return {"name": "Unknown User", "health_profile": "GENERAL"}

    def calculate_fit(self, user_id: str, product_data: Dict[str, Any], base_score: int) -> BioContextResult:
        user = self.fetch_user(user_id)
        profile = user["health_profile"]
        
        # Get nutrition values (default to 0 if missing)
        nutrition = product_data.get("nutrition", {})
        sugar = float(nutrition.get("sugar", {}).get("amount", 0))
        sodium = float(nutrition.get("sodium", {}).get("amount", 0))
        
        fit_score = base_score
        reasoning = f"Based on your {profile} profile, this is a standard match."

        if profile == "DIABETIC":
            if sugar > 10:
                fit_score = max(0, fit_score - 40)
                reasoning = f"SEVERE WARNING: High sugar content ({sugar}g) is extremely dangerous for your Diabetic profile."
            elif sugar > 5:
                fit_score = max(0, fit_score - 20)
                reasoning = "Moderate sugar content penalizes this score for your Diabetic profile."
            else:
                reasoning = "Low sugar content makes this a safe choice for your Diabetic profile."
                
        elif profile == "HYPERTENSION":
            if sodium > 400:
                fit_score = max(0, fit_score - 40)
                reasoning = f"SEVERE WARNING: High sodium ({sodium}mg) will elevate blood pressure."
            elif sodium > 200:
                fit_score = max(0, fit_score - 20)
                reasoning = "Moderate sodium content penalizes this score for your Hypertension profile."
            else:
                reasoning = "Low sodium content makes this safe for your blood pressure."

        return BioContextResult(
            user_name=user["name"],
            health_profile=profile,
            metabolic_fit_score=fit_score,
            context_reasoning=reasoning
        )
