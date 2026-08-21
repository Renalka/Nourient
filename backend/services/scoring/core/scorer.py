from core.models.product import ExtractedProductData, FoodDecisionProfile

class ScoringEngine:
    """
    Business logic for calculating the Food Decision Profile.
    This module strictly uses the UK Food Standards Agency (FSA) Nutrient Profiling System (the basis for Nutri-Score)
    and the NOVA classification system to provide scientifically grounded scores.
    """
    def calculate_score(self, product: ExtractedProductData) -> FoodDecisionProfile:
        nutrition = product.nutrition
        
        # Safe extraction of values, assuming per 100g basis
        protein_g = nutrition.protein.amount if (nutrition.protein and nutrition.protein.amount) else 0.0
        fiber_g = nutrition.fiber.amount if (nutrition.fiber and nutrition.fiber.amount) else 0.0
        sugar_g = nutrition.added_sugar.amount if (nutrition.added_sugar and nutrition.added_sugar.amount) else 0.0
        sodium_mg = nutrition.sodium.amount if (nutrition.sodium and nutrition.sodium.amount) else 0.0
        sat_fat_g = nutrition.saturated_fat.amount if (nutrition.saturated_fat and nutrition.saturated_fat.amount) else 0.0
        calories_kcal = nutrition.calories.amount if (nutrition.calories and nutrition.calories.amount) else 0.0
        energy_kj = calories_kcal * 4.184
        
        # 1. NUTRITIONAL QUALITY SCORE (FSA Nutrient Profiling System)
        
        # A Points (Negative Nutrients: 0-10 scale)
        points_energy = min(int(energy_kj / 335), 10)
        points_sat_fat = min(int(sat_fat_g / 1.0), 10)
        points_sugar = min(int(sugar_g / 4.5), 10)
        points_sodium = min(int(sodium_mg / 90), 10)
        a_points = points_energy + points_sat_fat + points_sugar + points_sodium
        
        # C Points (Positive Nutrients: 0-5 scale)
        points_protein = min(int(protein_g / 1.6), 5)
        points_fiber = min(int(fiber_g / 0.9), 5)
        # Assuming 0 fruits/veggies since we can't accurately parse exact percentages from standard labels without BigQuery
        c_points = points_fiber + points_protein
        
        # FSA Score Formula
        # A lower FSA score is healthier (range -15 to +40)
        fsa_score = a_points - c_points
        
        # Convert FSA Score (-15 to 40) to a 100-point scale for user readability (100 = Best)
        # Using min/max clamping to avoid bounds issues
        clamped_fsa = min(max(fsa_score, -15), 40)
        nutritional_quality_score = int(100 - (((clamped_fsa + 15) / 55) * 100))
        
        
        # 2. PROCESSING SCORE (NOVA Classification Approximation)
        # Group 1: Unprocessed (100)
        # Group 2: Processed culinary ingredients (80)
        # Group 3: Processed (50)
        # Group 4: Ultra-processed (20)
        
        ingredients_list = product.ingredients or []
        num_ingredients = len(ingredients_list)
        ingredients_lower = [i.lower() for i in ingredients_list]
        
        # Ultra-processed markers (NOVA Group 4)
        upf_markers = [
            "emulsifier", "artificial", "color", "flavor", "hydrogenated", 
            "hydrolysed", "maltodextrin", "syrup", "preservative", "sweetener", 
            "dextrose", "invert sugar", "isolate", "e2", "e3", "e4"
        ]
        
        is_ultra_processed = any(any(marker in ing for marker in upf_markers) for ing in ingredients_lower)
        
        if is_ultra_processed:
            processing_score = 20
        elif num_ingredients > 5:
            processing_score = 50
        elif num_ingredients > 1:
            processing_score = 80
        else:
            processing_score = 100
            
            
        # 3. OVERALL RECOMMENDATION
        # Combine Nutritional Quality and NOVA Processing
        avg_score = (nutritional_quality_score + processing_score) / 2
        
        reason_parts = []
        if is_ultra_processed:
            reason_parts.append("Contains ultra-processed ingredients (NOVA Group 4).")
        if fsa_score > 10:
            reason_parts.append("High in negative nutrients (sugar/sodium/sat fat) per the FSA model.")
        elif points_protein > 3 or points_fiber > 3:
            reason_parts.append("Good source of protein or fiber.")
            
        if avg_score > 75:
            rec = "EXCELLENT CHOICE"
        elif avg_score > 45:
            rec = "GOOD OCCASIONALLY"
        else:
            rec = "LIMIT CONSUMPTION"
            
        if not reason_parts:
            reason_parts.append("Moderate nutritional profile based on FSA profiling.")
            
        return FoodDecisionProfile(
            nutritional_quality_score=nutritional_quality_score,
            processing_score=processing_score,
            value_score=None,
            overall_recommendation=rec,
            reasoning=" ".join(reason_parts)
        )
