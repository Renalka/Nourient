import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# The entire block to remove
block_regex = r"                     \{\/\* Detailed Claims Audit \*\/\}[\s\S]*?No explicit marketing claims detected on the front of the packaging\.<\/p>\n                           <\/div>\n                         \)\}\n                       <\/div>\n                     <\/div>"

# Remove all instances
content = re.sub(block_regex, "", content)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
