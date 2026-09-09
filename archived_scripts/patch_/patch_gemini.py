with open('backend/services/extraction/core/ai_engine.py', 'r') as f:
    content = f.read()

content = content.replace("'gemini-1.5-flash'", "'gemini-2.5-flash'")

with open('backend/services/extraction/core/ai_engine.py', 'w') as f:
    f.write(content)

print("Restored model to gemini-2.5-flash")
