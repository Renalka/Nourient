from core.models.product import NutritionExtractionData, NutritionAnalysisData, AnalyzedServing, EmptyCalorieData, ThresholdWarning
import math

class NutritionEngine:
    def analyze(self, data: NutritionExtractionData) -> NutritionAnalysisData:
        if not data.raw_table or not data.stated_serving:
            return NutritionAnalysisData(error="NO_DATA", error_message="Missing nutrition data")

        # 1. Serving Size Loophole Exposer
        # Heuristic: If serving is very small (< 35g) and unit is 'g' or 'ml', people often eat more.
        # Average realistic snack session is ~50-100g.
        multiplier = 1.0
        is_loophole = False
        loophole_warning = ""
        realistic_amount = data.stated_serving.amount
        
        if data.stated_serving.amount < 35.0 and data.stated_serving.unit.lower() in ["g", "ml"]:
            multiplier = max(2.0, round(60.0 / data.stated_serving.amount, 1))
            realistic_amount = data.stated_serving.amount * multiplier
            is_loophole = True
            loophole_warning = f"The stated serving of {data.stated_serving.amount}{data.stated_serving.unit} ({data.stated_serving.description}) is unrealistically small. A normal portion is closer to {realistic_amount}{data.stated_serving.unit}."

        analyzed_serving = AnalyzedServing(
            realistic_amount=realistic_amount,
            unit=data.stated_serving.unit,
            is_loophole=is_loophole,
            loophole_warning=loophole_warning,
            multiplier=multiplier
        )

        # 2. Empty Calorie Ratio
        # Calories from sugar = sugar * 4, from sat fat = sat fat * 9
        # Per 100g basis
        table = data.raw_table
        empty_cals_100 = (table.sugar_per_100g * 4.0) + (table.sat_fat_per_100g * 9.0)
        total_cals_100 = table.calories_per_100g
        
        # Fiber + Protein + unsaturated fat = nutrient calories
        # Simplification:
        nutrient_cals_100 = total_cals_100 - empty_cals_100
        if nutrient_cals_100 < 0: nutrient_cals_100 = 0
        if total_cals_100 <= 0: total_cals_100 = 1 # avoid div by zero
        
        ratio = min(1.0, max(0.0, empty_cals_100 / total_cals_100))
        
        empty_cals = EmptyCalorieData(
            ratio=round(ratio, 2),
            empty_calories=round(empty_cals_100, 1),
            nutrient_calories=round(nutrient_cals_100, 1)
        )

        # 3. Threshold Warnings based on ADI
        # FDA/EFSA ADI: Sodium = 2300mg, Sugar = 50g
        warnings = []
        
        # Calculate amount in realistic serving
        realistic_sugar = (table.sugar_per_100g / 100.0) * realistic_amount
        realistic_sodium = (table.sodium_per_100g / 100.0) * realistic_amount
        
        sugar_adi = 50.0
        sodium_adi = 2300.0
        
        sugar_pct = (realistic_sugar / sugar_adi) * 100
        if sugar_pct > 30.0:
            warnings.append(ThresholdWarning(
                nutrient="Added Sugars",
                amount_in_realistic_serving=round(realistic_sugar, 1),
                unit="g",
                percentage_of_adi=round(sugar_pct, 1),
                warning_message=f"One realistic portion contains {round(sugar_pct)}% of your daily sugar limit."
            ))
            
        sodium_pct = (realistic_sodium / sodium_adi) * 100
        if sodium_pct > 25.0:
            warnings.append(ThresholdWarning(
                nutrient="Sodium",
                amount_in_realistic_serving=round(realistic_sodium, 1),
                unit="mg",
                percentage_of_adi=round(sodium_pct, 1),
                warning_message=f"One realistic portion contains {round(sodium_pct)}% of your daily sodium limit."
            ))

        return NutritionAnalysisData(
            stated_serving=data.stated_serving,
            analyzed_serving=analyzed_serving,
            empty_calorie_ratio=empty_cals,
            threshold_warnings=warnings
        )
