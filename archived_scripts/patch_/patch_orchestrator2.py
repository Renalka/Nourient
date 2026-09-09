import re

with open('backend/services/orchestrator/api/routes.py', 'r') as f:
    content = f.read()

old_logic = """            # 3. Decode Ingredients (Mocked for Claims Engine)
            decoded_ingredients = [{"name": ing} for ing in raw_ingredients]
            
            # 4. Verify Claims
            verify_payload = {
                "explicit_claims": explicit_claims,
                "ingredients": decoded_ingredients
            }"""

new_logic = """            # 3. Use raw ingredients directly (they are already dicts with 'name')
            decoded_ingredients = raw_ingredients
            
            # 4. Verify Claims
            verify_payload = {
                "explicit_claims": explicit_claims,
                "ingredients": decoded_ingredients
            }"""

content = content.replace(old_logic, new_logic)

with open('backend/services/orchestrator/api/routes.py', 'w') as f:
    f.write(content)
