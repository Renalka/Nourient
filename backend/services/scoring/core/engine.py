import os
import joblib
from typing import Dict, Any

class ScoringEngine:
    def __init__(self):
        self.upf_model = None
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "upf_model_v2.pkl")
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

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Handle both old payloads (just extracted_data) and new dual payloads
        extracted_data = payload.get("extracted_data", payload)
        detective_data = payload.get("detective_data", {})
        
        nutrition = extracted_data.get("nutrition", {})
        
        # 1. Deterministic Nutri-Score (FSA)
        fsa_score = self.calculate_fsa_score(nutrition)
        grade = self.get_nutriscore_grade(fsa_score)
        
        if grade == "A": quality_score = 95
        elif grade == "B": quality_score = 80
        elif grade == "C": quality_score = 65
        elif grade == "D": quality_score = 45
        else: quality_score = 20
        
        # 2. Advanced Multi-Feature ML Prediction (NOVA / Processing Score)
        processing_score = 50 # Default safe fallback
        upf_probability = None
        nova_group = "NOVA 3 (Processed)"
        
        if self.upf_model:
            try:
                calories = float(nutrition.get("calories", {}).get("amount", 0) or 0)
                sugar = float(nutrition.get("sugar", {}).get("amount", 0) or 0)
                sodium = float(nutrition.get("sodium", {}).get("amount", 0) or 0)
                sat_fat = float(nutrition.get("saturated_fat", {}).get("amount", 0) or 0)
                protein = float(nutrition.get("protein", {}).get("amount", 0) or 0)
                fiber = float(nutrition.get("fiber", {}).get("amount", 0) or 0)
                
                # Parse Detective Data for Safety Features
                decoded_additives = detective_data.get("decoded_additives", [])
                total_ingredients = len(decoded_additives) if decoded_additives else len(extracted_data.get("ingredients", []))
                
                synthetic = sum(1 for item in decoded_additives if item.get("source", "").lower() == "synthetic / processed")
                high_risk = sum(1 for item in decoded_additives if item.get("risk_level", "").lower() == "high risk")
                moderate_risk = sum(1 for item in decoded_additives if item.get("risk_level", "").lower() == "moderate risk")
                natural = sum(1 for item in decoded_additives if item.get("source", "").lower() in ["natural", "natural derived"])
                
                # Construct 11-Dimensional Feature Vector
                X = [[
                    calories, sugar, sodium, sat_fat, protein, fiber,
                    total_ingredients, synthetic, high_risk, moderate_risk, natural
                ]]
                
                # Predict continuous Processing & Health Score (0-100)
                predicted_score = self.upf_model.predict(X)[0]
                processing_score = int(max(0, min(100, predicted_score)))
                upf_probability = 100 - processing_score # Just for backwards compatibility flag
                
                if processing_score >= 80:
                    formulation_tier = "Clean & Wholesome"
                elif processing_score >= 40:
                    formulation_tier = "Moderately Processed"
                else:
                    formulation_tier = "Highly Processed"
                    
            except Exception as e:
                print(f"ML Inference Error: {e}")
        
        recommendation = "CONSUME FREQUENTLY"
        if quality_score < 40 or processing_score < 40:
            recommendation = "LIMIT CONSUMPTION"
        elif quality_score < 70 or processing_score < 70:
            recommendation = "CONSUME IN MODERATION"

        reasoning = f"Nutritional Grade: {grade}. Formulation quality is {formulation_tier}."
        if upf_probability is not None:
            reasoning += f" Comprehensive AI Score ({processing_score}/100) incorporates both macros and ingredient toxicity."

        return {
            "nutritional_quality_score": quality_score,
            "processing_score": processing_score,
            "value_score": None,
            "overall_recommendation": recommendation,
            "reasoning": reasoning
        }
