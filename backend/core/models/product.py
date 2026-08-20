from pydantic import BaseModel, Field
from typing import List, Optional

class NutritionFact(BaseModel):
    amount: float
    unit: str

class NutritionInfo(BaseModel):
    calories: Optional[NutritionFact] = None
    protein: Optional[NutritionFact] = None
    carbohydrates: Optional[NutritionFact] = None
    added_sugar: Optional[NutritionFact] = None
    fiber: Optional[NutritionFact] = None

class ProductBase(BaseModel):
    name: str
    brand: str
    category: str
    price: Optional[float] = None

class ExtractedProductData(ProductBase):
    """
    Data Transfer Object (DTO) representing the structured output
    expected from the Gemini Vision OCR service.
    """
    ingredients: List[str] = Field(default_factory=list, description="Parsed list of ingredients")
    claims: List[str] = Field(default_factory=list, description="Marketing claims found on packaging")
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
