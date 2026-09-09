import re

with open('backend/scripts/pinecone_ingredients_etl.py', 'r') as f:
    content = f.read()

# Add unicodedata import
if "import unicodedata" not in content:
    content = content.replace("import re", "import re\nimport unicodedata")

# Replace ID generation lines
content = content.replace('ids.append(f"add_{code}_{i}")', 'raw_id = f"add_{code}_{i}"\n            safe_id = unicodedata.normalize("NFKD", raw_id).encode("ASCII", "ignore").decode("utf-8")\n            ids.append(safe_id)')

content = content.replace('ids.append(f"ing_{key.replace(\':\', \'_\')}_{i}")', 'raw_id = f"ing_{key.replace(\':\', \'_\')}_{i}"\n            safe_id = unicodedata.normalize("NFKD", raw_id).encode("ASCII", "ignore").decode("utf-8")\n            safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", safe_id)\n            ids.append(safe_id)')

# Add skip logic for already processed batches
loop_start = "for i in range(0, len(docs), batch_size):"
loop_replace = """    start_batch = 228  # Batch 229 failed, so we start at index 228 * 100
    print(f"Resuming from batch {start_batch + 1} to avoid repeating work...")
    
    for i in range(start_batch * batch_size, len(docs), batch_size):"""

if loop_start in content:
    content = content.replace(loop_start, loop_replace)

with open('backend/scripts/pinecone_ingredients_etl.py', 'w') as f:
    f.write(content)

print("Patched successfully.")
