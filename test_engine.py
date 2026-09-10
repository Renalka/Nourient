from backend.services.alternatives.core.engine import AlternativesEngine
import logging
logging.basicConfig(level=logging.INFO)
engine = AlternativesEngine()
results = engine.find_better_alternatives("snack", current_sugar=15.0, current_protein=2.0)
print(f"RESULTS LENGTH: {len(results)}")
print(results)
