with open('backend/services/auditor/core/agent.py', 'r') as f:
    content = f.read()

content = content.replace("'gemini-2.5-flash'", "'gemini-3.5-flash'")

with open('backend/services/auditor/core/agent.py', 'w') as f:
    f.write(content)
