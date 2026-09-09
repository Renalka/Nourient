import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. Add uploadInputRef2
ref1 = "  const uploadInputRef = useRef<HTMLInputElement>(null);"
ref2 = "  const uploadInputRef = useRef<HTMLInputElement>(null);\n  const uploadInputRef2 = useRef<HTMLInputElement>(null);"
if "uploadInputRef2" not in content:
    content = content.replace(ref1, ref2)

# 2. Add handleFile2Change
handle1 = """  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
      setStep(2);
    }
  };"""

handle2 = handle1 + """

  const handleFile2Change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile2(selected);
      setPreviewUrl2(URL.createObjectURL(selected));
      setStep(2);
    }
  };"""

if "handleFile2Change" not in content:
    content = content.replace(handle1, handle2)

# 3. Add the actual hidden input for ref2 in the JSX
input1 = """                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef}
                     onChange={handleFileChange}
                     className="hidden"
                   />"""

input2 = input1 + """
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef2}
                     onChange={handleFile2Change}
                     className="hidden"
                   />"""

if "uploadInputRef2" not in content.split("Right Viewfinder")[1]:
    content = content.replace(input1, input2)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
