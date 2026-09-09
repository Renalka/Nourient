import os

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if "from dotenv import load_dotenv" not in content:
        # insert it right after import os
        content = content.replace("import os", "import os\nfrom dotenv import load_dotenv\nload_dotenv()")
        
        with open(filepath, 'w') as f:
            f.write(content)

patch_file('backend/scripts/pinecone_etl.py')
patch_file('backend/services/detective/core/claims_engine.py')
