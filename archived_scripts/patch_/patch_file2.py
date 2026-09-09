import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

handle2 = """  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile(compressed);
      setPreviewUrl(URL.createObjectURL(compressed));
      setStep(2);
    }
  };

  const handleFile2Change = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      setStep(2);
    }
  };"""

content = re.sub(r"  const handleFileChange = async \(e: React.ChangeEvent<HTMLInputElement>\) => {[\s\S]*?  };", handle2, content)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
