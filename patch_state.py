import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_state = """  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);"""

new_state = """  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [previewUrl2, setPreviewUrl2] = useState<string | null>(null);"""

if "setFile2" not in content:
    content = content.replace(old_state, new_state)
    with open('frontend/src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
    print("Added file2 and previewUrl2 to state")
else:
    print("Already in state")
