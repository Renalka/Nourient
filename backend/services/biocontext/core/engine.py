from pydantic import BaseModel
from typing import Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-adminsdk.json')
    firebase_admin.initialize_app(cred, options={'projectId': 'nourient-38381'})

class BioContextResult(BaseModel):
    user_name: str
    health_profile: str
    metabolic_fit_score: int
    context_reasoning: str

class BioContextEngine:
    def __init__(self):
        self.db = firestore.client()
        self.collection_name = 'users'

    def fetch_user(self, user_id: str) -> Dict[str, str]:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return {"name": data.get("name", "Authenticated User"), "health_profile": data.get("health_profile", "GENERAL")}
        return {"name": "Unknown User", "health_profile": "GENERAL"}

    def update_user_profile(self, user_id: str, health_profile: str) -> bool:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc_ref.set({
            "name": "Authenticated User",
            "health_profile": health_profile
        }, merge=True)
        return True

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
