import os
import joblib
from typing import Dict, Any

class ScoringEngine:
    def __init__(self):
        self.upf_model = None
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "upf_model.pkl")
        if os.path.exists(model_path):
            try:
                self.upf_model = joblib.load(model_path)
            except Exception as e:
                print(f"Failed to load ML model: {e}")

    def calculate_fsa_score(self, nutrition: Dict[str, Any]) -> int:
        """
        Calculates a simplified FSA (Food Standards Agency) Nutri-Score baseline.
        """
        energy_kj = float(nutrition.get("calories", {}).get("amount", 0) or 0) * 4.184
        sugar_g = float(nutrition.get("sugar", {}).get("amount", 0) or 0)
        sodium_mg = float(nutrition.get("sodium", {}).get("amount", 0) or 0)
        sat_fat_g = float(nutrition.get("saturated_fat", {}).get("amount", 0) or 0)
        protein_g = float(nutrition.get("protein", {}).get("amount", 0) or 0)
        fiber_g = float(nutrition.get("fiber", {}).get("amount", 0) or 0)

        points_a = min(10, int(energy_kj / 335)) + min(10, int(sugar_g / 4.5)) + min(10, int(sat_fat_g / 1)) + min(10, int(sodium_mg / 90))
        points_c = min(5, int(protein_g / 1.6)) + min(5, int(fiber_g / 0.9))

        return points_a - points_c

    def get_nutriscore_grade(self, fsa_score: int) -> str:
        if fsa_score <= -1: return "A"
        if fsa_score <= 2: return "B"
        if fsa_score <= 10: return "C"
        if fsa_score <= 18: return "D"
        return "E"

    def evaluate(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        nutrition = extracted_data.get("nutrition", {})
        ingredients = extracted_data.get("ingredients", [])
        
        # 1. Deterministic Nutri-Score (FSA)
        fsa_score = self.calculate_fsa_score(nutrition)
        grade = self.get_nutriscore_grade(fsa_score)
        
        if grade == "A": quality_score = 95
        elif grade == "B": quality_score = 80
        elif grade == "C": quality_score = 65
        elif grade == "D": quality_score = 45
        else: quality_score = 20
        
        # 2. Sophisticated Machine Learning Prediction (NOVA / UPF)
        processing_score = max(0, 100 - (len(ingredients) * 5)) # Fallback heuristic
        upf_probability = None
        
        if self.upf_model:
            try:
                X = [[
                    float(nutrition.get("calories", {}).get("amount", 0) or 0),
                    float(nutrition.get("sugar", {}).get("amount", 0) or 0),
                    float(nutrition.get("sodium", {}).get("amount", 0) or 0),
                    float(nutrition.get("saturated_fat", {}).get("amount", 0) or 0),
                    float(nutrition.get("protein", {}).get("amount", 0) or 0),
                    float(nutrition.get("fiber", {}).get("amount", 0) or 0)
                ]]
                proba = self.upf_model.predict_proba(X)[0]
                upf_probability = int(proba[1] * 100)
                # Convert the UPF Probability directly into a Data-Grounded Processing Score
                # 100% UPF = 0/100 Processing Score. 0% UPF = 100/100 Processing Score.
                processing_score = 100 - upf_probability
            except Exception as e:
                print(f"ML Inference Error: {e}")
        
        recommendation = "CONSUME FREQUENTLY"
        if quality_score < 40 or processing_score < 40:
            recommendation = "LIMIT CONSUMPTION"
        elif quality_score < 70:
            recommendation = "CONSUME IN MODERATION"

        reasoning = f"Nutritional Grade: {grade}."
        if upf_probability is not None:
            reasoning += f" Processing Score ({processing_score}/100) generated via Machine Learning."

        return {
            "nutritional_quality_score": quality_score,
            "processing_score": processing_score,
            "value_score": None,
            "overall_recommendation": recommendation,
            "reasoning": reasoning
        }
