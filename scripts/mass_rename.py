import os

def is_text_file(filepath):
    try:
        with open(filepath, 'tr') as check_file:
            check_file.read(1024)
            return True
    except:
        return False

skip_dirs = {'.git', 'node_modules', '.next', 'venv', '__pycache__', '.gemini'}

files_changed = 0

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for root, dirs, files in os.walk(root_dir):
    # Modify dirs in-place to skip hidden/build directories
    dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
    
    for file in files:
        if file == 'mass_rename.py' or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.ico'):
            continue
            
        filepath = os.path.join(root, file)
        
        if not is_text_file(filepath):
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Protect Pinecone indexes
            content = content.replace("patchamomma-ingredients", "__PINECONE_ING__")
            content = content.replace("patchamomma-claims", "__PINECONE_CLAIMS__")
            
            # Standard renames
            content = content.replace("Patchamomma", "Nourient")
            content = content.replace("patchamomma", "nourient")
            content = content.replace("PATCHAMOMMA", "NOURIENT")
            
            # Restore Pinecone indexes
            content = content.replace("__PINECONE_ING__", "patchamomma-ingredients")
            content = content.replace("__PINECONE_CLAIMS__", "patchamomma-claims")
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_changed += 1
                
        except Exception as e:
            print(f"Skipping {filepath} due to error: {e}")

print(f"Successfully renamed across {files_changed} files.")
