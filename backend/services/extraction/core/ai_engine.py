import google.generativeai as genai
import json
from typing import Any, Dict, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.interfaces import IAIEngine
from core.config import settings

class GeminiEngine(IAIEngine):
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # 2026 Compatible Model: gemini-2.5-flash (or gemini-flash-latest)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    async def extract_structured_data(self, image_bytes: bytes, prompt: str, response_schema: Any = None) -> Dict[str, Any]:
        """
        Extracts structured JSON from an image using Gemini Vision.
        """
        import asyncio
        from google.api_core.exceptions import DeadlineExceeded

        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ]
        
        # Enforcing JSON format for modern models
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
        
        # Add a retry loop for 504 timeouts
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.model.generate_content_async(
                    contents=[prompt, image_parts[0]],
                    generation_config=generation_config
                )
                break # Success! Break the loop
            except DeadlineExceeded as e:
                if attempt == max_retries - 1:
                    raise e # Exhausted retries
                await asyncio.sleep(2) # Backoff before retrying
                print(f"Vision AI Timeout (Attempt {attempt + 1}). Retrying...")
        
        text = response.text
        # Safety net: clean markdown code blocks if the AI returns them despite mime_type
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())

    async def audit_claims(self, claims: List[str], ingredients: List[str]) -> Dict[str, Any]:
        pass
