with open('backend/services/orchestrator/api/routes.py', 'r') as f:
    content = f.read()

content = content.replace("timeout=60.0", "timeout=120.0")

with open('backend/services/orchestrator/api/routes.py', 'w') as f:
    f.write(content)
