import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

content = content.replace('"{c.claim}"', '&quot;{c.claim}&quot;')
content = content.replace('"{l.claim}"', '&quot;{l.claim}&quot;')
content = content.replace('"{b.word}"', '&quot;{b.word}&quot;')

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
