import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

retake_old = """  const handleRetake = () => {
    setFile(null);
    setPreviewUrl(null);
    setStep(1);
    setError(null);
  };"""

retake_new = """  const handleRetake = () => {
    setFile(null);
    setPreviewUrl(null);
    setFile2(null);
    setPreviewUrl2(null);
    setStep(1);
    setError(null);
  };"""

content = content.replace(retake_old, retake_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
