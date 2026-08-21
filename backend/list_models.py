import google.generativeai as genai
import os
from core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    models = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            models.append(m.name)
    print("SUPPORTED MODELS:", models)
except Exception as e:
    print("ERROR listing models:", e)
