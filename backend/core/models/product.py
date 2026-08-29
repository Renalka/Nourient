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

class FoodDecisionProfile(BaseModel):
    """
    DTO for the multi-dimensional Food Quality Score (Feature 1).
    """
    nutritional_quality_score: int
    processing_score: int
    value_score: Optional[int] = None
    overall_recommendation: str
    reasoning: str
