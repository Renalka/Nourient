import google.generativeai as genai
import json
import logging
from typing import Dict, Any, List
from core.config import settings
from core.models.product import ExtractedProductData, TrueLabelAuditResult, ClaimVerdict

logger = logging.getLogger(__name__)

class AuditorAgent:
    """
    TrueLabel Auditor AI (Feature 12).
    Uses the Gemini 2.5 Flash model to perform fast reasoning, 
    comparing front-of-pack marketing claims against the actual ingredients list.
    """
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Downgrading to the Flash model to bypass Free Tier Pro limits (limit: 0)
        self.model = genai.GenerativeModel('gemini-3.5-flash')
        logger.info("Initialized AuditorAgent with gemini-2.5-flash (Quota Workaround)")

    async def audit_product(self, product: ExtractedProductData) -> TrueLabelAuditResult:
        logger.info(f"Starting audit for product: '{product.name}'")
        
        if not product.claims or not product.ingredients:
            logger.info("Skipping audit: No claims or ingredients provided.")
            return TrueLabelAuditResult(
                product_name=product.name,
                overall_trust_score=100,
                verdicts=[ClaimVerdict(claim="No claims to audit", status="VERIFIED", reasoning="Nothing to check.")]
            )
            
        # Extract names for the prompt
        ingredient_names = [i.name for i in product.ingredients if i.name]
        
        prompt = f"""
        You are a strict, adversarial food regulatory auditor working for the FDA/FSSAI.
        Your job is to expose 'greenwashing' and deceptive marketing on food packaging.
        
        Product: {product.name}
        Marketing Claims on the front: {product.claims}
        Actual Ingredients List on the back: {ingredient_names}
        
        Analyze EACH claim against the ingredients. Look for loopholes. 
        For example: If the claim is 'No Added Sugar', but the ingredients contain 'Apple Juice Concentrate', 'Maltodextrin', or 'Honey', that is DECEPTIVE.
        If the claim is 'Made with Real Fruit', but fruit is the 10th ingredient behind artificial flavors, that is MISLEADING.
        
        Return your strict analysis strictly in the following JSON format:
        {{
            "overall_trust_score": 80,
            "verdicts": [
                {{
                    "claim": "The exact claim",
                    "status": "VERIFIED", // Must be exactly VERIFIED, DECEPTIVE, or MISLEADING
                    "reasoning": "A concise, 1-sentence explanation of why, referencing specific ingredients."
                }}
            ]
        }}
        """
        
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
        
        logger.info(f"Sending prompt to Gemini 3.1 Pro. Evaluating {len(product.claims)} claims...")
        
        try:
            response = await self.model.generate_content_async(
                contents=[prompt],
                generation_config=generation_config
            )
            logger.info("Successfully received response from Gemini 3.1 Pro.")
            
            text = response.text
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            result_dict = json.loads(text.strip())
            logger.info(f"Parsed JSON audit result: Trust Score {result_dict.get('overall_trust_score')}")
            
            # Parse into Pydantic models
            verdicts = [ClaimVerdict(**v) for v in result_dict.get("verdicts", [])]
            
            return TrueLabelAuditResult(
                product_name=product.name,
                overall_trust_score=result_dict.get("overall_trust_score", 50),
                verdicts=verdicts
            )
            
        except Exception as e:
            logger.error(f"CRITICAL ERROR in Auditor Agent: {str(e)}", exc_info=True)
            raise e
