import re

with open('backend/services/extraction/api/routes.py', 'r') as f:
    content = f.read()

old_json = """  "prominent_ingredients": [
    {
      "name": "e.g. Real Strawberries",
      "implied_quantity": "Showcased as the primary ingredient via massive imagery",
      "reality_check": "Often makes up < 1% of the formulation. Check the ingredients list to verify."
    }
  ],
  "error": null,
  "error_message": null
}"""

new_json = """  "prominent_ingredients": [
    {
      "name": "e.g. Real Strawberries",
      "implied_quantity": "Showcased as the primary ingredient via massive imagery",
      "reality_check": "Often makes up < 1% of the formulation. Check the ingredients list to verify."
    }
  ],
  "explicit_claims": ["100% Natural", "No Added Sugar", "Farm Fresh"],
  "error": null,
  "error_message": null
}"""

content = content.replace(old_json, new_json)

instruction_old = """2. Only populate 'prominent_ingredients' if the packaging explicitly showcases a premium ingredient (like fruit, honey, oats) using large text or pictures."""
instruction_new = """2. Only populate 'prominent_ingredients' if the packaging explicitly showcases a premium ingredient (like fruit, honey, oats) using large text or pictures.
3. Extract any explicit textual marketing claims made on the front into 'explicit_claims' (e.g. "Keto Friendly", "Gluten Free", "Organic")."""

content = content.replace(instruction_old, instruction_new).replace("3. If the image is not a food", "4. If the image is not a food")

with open('backend/services/extraction/api/routes.py', 'w') as f:
    f.write(content)

