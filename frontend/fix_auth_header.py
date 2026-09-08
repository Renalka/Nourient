import re

with open('src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

target = """      const token = await getToken();
      const idToken = token || 'anonymous';
      
      const endpoint = isEnhanced 
        ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner'
        : 'http://localhost:8003/api/v1/orchestrate/scanner';

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${idToken}` },
        body: formData,
      });"""

replacement = """      const token = await getToken();
      
      const endpoint = isEnhanced 
        ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner'
        : 'http://localhost:8003/api/v1/orchestrate/scanner';

      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: formData,
      });"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
    print("Replaced exact target successfully.")
else:
    print("Target block not found. Trying regex.")
    # Fallback if there are minor whitespace differences
    regex_target = r"const idToken = token \|\| 'anonymous';\s+const endpoint = (.*?);\s+const response = await fetch\(endpoint, \{\s+method: 'POST',\s+headers: \{ 'Authorization': `Bearer \$\{idToken\}` \},\s+body: formData,\s+\}\);"
    regex_repl = r"const endpoint = \1;\n\n      const headers: Record<string, string> = {};\n      if (token) {\n        headers['Authorization'] = `Bearer ${token}`;\n      }\n\n      const response = await fetch(endpoint, {\n        method: 'POST',\n        headers,\n        body: formData,\n      });"
    
    new_content = re.sub(regex_target, regex_repl, content, flags=re.DOTALL)
    if new_content != content:
        with open('src/app/scanner/page.tsx', 'w') as f:
            f.write(new_content)
        print("Replaced via regex successfully.")
    else:
        print("Could not find the block to replace.")
