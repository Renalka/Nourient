import re

with open('backend/services/detective/core/claims_engine.py', 'r') as f:
    content = f.read()

content = content.replace("flavor enhancer,", "flavor enhancer, flavour enhancer,")

with open('backend/services/detective/core/claims_engine.py', 'w') as f:
    f.write(content)
