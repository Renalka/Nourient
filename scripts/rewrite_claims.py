import os
import re

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(root_dir, 'frontend/src/app/scanner/page.tsx')

with open(file_path, 'r') as f:
    content = f.read()

# 1. State changes
state_old = "const [isCameraActive, setIsCameraActive] = useState(false);"
state_new = "const [isCameraActive, setIsCameraActive] = useState(false);\n  const [activeClaimsTab, setActiveClaimsTab] = useState<'front' | 'back'>('front');"
content = content.replace(state_old, state_new)


# 2. handleFileChange
filechange_old = """  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const url = URL.createObjectURL(selectedFile);
      setPreviewUrl(url);
    }
  };"""

filechange_new = """  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (scanMode === 'claims' && activeClaimsTab === 'back') {
        setFile2(selectedFile);
        setPreviewUrl2(URL.createObjectURL(selectedFile));
      } else {
        setFile(selectedFile);
        setPreviewUrl(URL.createObjectURL(selectedFile));
      }
    }
  };"""
content = content.replace(filechange_old, filechange_new)

with open(file_path, 'w') as f:
    f.write(content)
print("Updated frontend scanner page.tsx")
