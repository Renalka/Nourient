import re

with open('backend/services/detective/core/claims_engine.py', 'r') as f:
    content = f.read()

old_patterns = """            {
                "id": "p6",
                "text": "Made with Real Fruit",
                "meta": {"type": "loophole", "targets": "fruit juice concentrate, fruit puree", "explanation": "'Real fruit' is often just a highly processed fruit juice concentrate stripped of fiber and behaving identically to added sugar."}
            }
        ]"""

new_patterns = """            {
                "id": "p6",
                "text": "Made with Real Fruit",
                "meta": {"type": "loophole", "targets": "fruit juice concentrate, fruit puree", "explanation": "'Real fruit' is often just a highly processed fruit juice concentrate stripped of fiber and behaving identically to added sugar."}
            },
            {
                "id": "p7",
                "text": "No Artificial Flavors",
                "meta": {"type": "contradiction", "targets": "artificial flavor, synthetic flavor, flavor enhancer, msg, monosodium glutamate, disodium inosinate, disodium guanylate, ins 627, ins 631, ins 621", "explanation": "Found synthetic flavor enhancers despite 'No Artificial Flavors' claim."}
            },
            {
                "id": "p8",
                "text": "No Artificial Colors",
                "meta": {"type": "contradiction", "targets": "red 40, yellow 5, yellow 6, blue 1, blue 2, green 3, artificial color, synthetic color, caramel color", "explanation": "Found artificial food dyes despite 'No Artificial Colors' claim."}
            },
            {
                "id": "p9",
                "text": "No Artificial Flavors or Colors",
                "meta": {"type": "contradiction", "targets": "artificial flavor, synthetic flavor, flavor enhancer, msg, monosodium glutamate, disodium inosinate, disodium guanylate, ins 627, ins 631, ins 621, red 40, yellow 5, yellow 6, blue 1, blue 2, green 3, artificial color, synthetic color, caramel color", "explanation": "Found synthetic flavor enhancers or artificial food dyes despite the 'No Artificial Flavors or Colors' claim."}
            }
        ]"""

content = content.replace(old_patterns, new_patterns)

with open('backend/services/detective/core/claims_engine.py', 'w') as f:
    f.write(content)
