import re

with open('backend/services/detective/core/claims_engine.py', 'r') as f:
    content = f.read()

# Replace `query_emb = self.emb_fn([claim])[0]` with `query_emb = self.emb_fn([claim])[0]` converted to list
old_code = "query_emb = self.emb_fn([claim])[0]"
new_code = "query_emb = self.emb_fn([claim])[0]\n            if hasattr(query_emb, 'tolist'):\n                query_emb = query_emb.tolist()"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('backend/services/detective/core/claims_engine.py', 'w') as f:
        f.write(content)
    print("Patched successfully.")
else:
    print("Could not find the target string.")
