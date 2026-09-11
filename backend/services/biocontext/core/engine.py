from pydantic import BaseModel
from typing import Dict, Any
import firebase_admin
from firebase_admin import firestore
from core.gcp import initialize_firebase_admin

initialize_firebase_admin()

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
        
        nutrition = product_data.get("nutrition", {})
        sugar = float(nutrition.get("sugar", {}).get("amount", 0) or 0)
        sodium = float(nutrition.get("sodium", {}).get("amount", 0) or 0)
        sat_fat = float(nutrition.get("saturated_fat", {}).get("amount", 0) or 0)
        fiber = float(nutrition.get("fiber", {}).get("amount", 0) or 0)
        protein = float(nutrition.get("protein", {}).get("amount", 0) or 0)
        
        fit_score = base_score
        reasoning_points = []

        if profile == "DIABETIC":
            if sugar > 15:
                fit_score -= 50
                reasoning_points.append(f"SEVERE DANGER: {sugar}g sugar is extremely dangerous for your blood glucose.")
            elif sugar > 5:
                fit_score -= 25
                reasoning_points.append(f"High sugar ({sugar}g) penalizes this item heavily.")
            elif sugar <= 2 and fiber >= 3:
                fit_score += 15
                reasoning_points.append("Excellent low-sugar/high-fiber ratio for glycemic control.")
                
        elif profile == "HYPERTENSION":
            if sodium > 400:
                fit_score -= 50
                reasoning_points.append(f"SEVERE DANGER: {sodium}mg sodium will violently spike blood pressure.")
            elif sodium > 200:
                fit_score -= 25
                reasoning_points.append(f"High sodium ({sodium}mg) makes this a poor choice.")
            if sat_fat > 5:
                fit_score -= 15
                reasoning_points.append("High saturated fat adds secondary cardiovascular risk.")
            if sodium < 100:
                fit_score += 10
                reasoning_points.append("Low sodium content makes this heart-safe.")

        elif profile == "GENERAL":
            # Just generally reward good macros and punish bad ones slightly to make the score 'dynamic'
            if protein > 10:
                fit_score += 10
                reasoning_points.append("Good source of protein.")
            if fiber > 5:
                fit_score += 10
                reasoning_points.append("High fiber content supports digestion.")
            if sugar > 20:
                fit_score -= 20
                reasoning_points.append("Excessive added sugars detract from overall wellness.")

        # Ensure bounds
        fit_score = max(0, min(100, fit_score))
        
        reasoning = " ".join(reasoning_points) if reasoning_points else f"Standard match for {profile} profile."

        return BioContextResult(
            user_name=user["name"],
            health_profile=profile,
            metabolic_fit_score=fit_score,
            context_reasoning=reasoning
        )
