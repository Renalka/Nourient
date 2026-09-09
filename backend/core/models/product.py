from pydantic import BaseModel
from typing import List, Optional

class NutritionFact(BaseModel):
    amount: float
    unit: str

class NutritionInfo(BaseModel):
    calories: Optional[NutritionFact]
    protein: Optional[NutritionFact]
    carbohydrates: Optional[NutritionFact]
    sugar: Optional[NutritionFact]
    fiber: Optional[NutritionFact]
    sodium: Optional[NutritionFact]
    saturated_fat: Optional[NutritionFact]

class ProductBase(BaseModel):
    name: str
    brand: str
    category: str
    price: Optional[float]

class ClaimVerdict(BaseModel):
    claim: str
    status: str # "VERIFIED", "DECEPTIVE", "MISLEADING"
    reasoning: str

class TrueLabelAuditResult(BaseModel):
    product_name: str
    overall_trust_score: int # 0-100
    verdicts: List[ClaimVerdict]

class IngredientDetail(BaseModel):
    name: str
    ins_code: Optional[str] = None
    percentage: Optional[float] = None
    
class ExtractedProductData(ProductBase):
    """
    Data Transfer Object (DTO) representing the structured output
    expected from the Gemini Vision OCR service.
    """
    ingredients: List[IngredientDetail]
    claims: List[str]
    nutrition: NutritionInfo
    error: Optional[str] = None
    error_message: Optional[str] = None

class FoodDecisionProfile(BaseModel):
    """
    DTO for the multi-dimensional Food Quality Score (Feature 1).
    """
    nutritional_quality_score: int
    processing_score: int
    value_score: Optional[int] = None
    overall_recommendation: str
    reasoning: str

class HealthHalo(BaseModel):
    visual_cues: List[str]
    deception_index: int
    reasoning: str

class TargetAudience(BaseModel):
    demographic: str
    indicators: List[str]
    concerns: List[str]

class ProminentIngredient(BaseModel):
    name: str
    implied_quantity: str
    reality_check: str

class FrontOfPackData(BaseModel):
    health_halo: Optional[HealthHalo] = None
    target_audience: Optional[TargetAudience] = None
    prominent_ingredients: List[ProminentIngredient] = []
    explicit_claims: List[str] = []
    error: Optional[str] = None
    error_message: Optional[str] = None

class StatedServing(BaseModel):
    amount: float
    unit: str
    description: str

class AnalyzedServing(BaseModel):
    realistic_amount: float
    unit: str
    is_loophole: bool
    loophole_warning: str
    multiplier: float

class EmptyCalorieData(BaseModel):
    ratio: float
    empty_calories: float
    nutrient_calories: float

class ThresholdWarning(BaseModel):
    nutrient: str
    amount_in_realistic_serving: float
    unit: str
    percentage_of_adi: float
    warning_message: str

class RawNutritionTable(BaseModel):
    calories_per_100g: float
    sugar_per_100g: float
    fiber_per_100g: float
    protein_per_100g: float
    sodium_per_100g: float
    fat_per_100g: float
    sat_fat_per_100g: float

class NutritionExtractionData(BaseModel):
    stated_serving: Optional[StatedServing] = None
    raw_table: Optional[RawNutritionTable] = None
    error: Optional[str] = None
    error_message: Optional[str] = None

class NutritionAnalysisData(BaseModel):
    stated_serving: Optional[StatedServing] = None
    analyzed_serving: Optional[AnalyzedServing] = None
    empty_calorie_ratio: Optional[EmptyCalorieData] = None
    threshold_warnings: List[ThresholdWarning] = []
    error: Optional[str] = None
    error_message: Optional[str] = None
