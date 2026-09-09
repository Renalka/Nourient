with open('backend/services/extraction/api/routes.py', 'r') as f:
    content = f.read()

old_inst = "1. Extract a clean, deduplicated list of ingredients."
new_inst = "1. Extract the exact ingredients list verbatim. DO NOT summarize, drop, or truncate synonyms in parentheses. If it says 'Refined Wheat Flour (Maida)', the name MUST be extracted exactly as 'Refined Wheat Flour (Maida)'."

content = content.replace(old_inst, new_inst)

with open('backend/services/extraction/api/routes.py', 'w') as f:
    f.write(content)

print("Patched the extraction prompt for verbatim ingredients")
