import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

cap_old = """        canvas.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
            setFile(capturedFile);
            setPreviewUrl(URL.createObjectURL(capturedFile));
            stopCamera();
            setStep(2);
          }
        }, 'image/jpeg', 0.7);"""

cap_new = """        canvas.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
            if (scanMode === 'claims' && activeClaimsTab === 'back') {
              setFile2(capturedFile);
              setPreviewUrl2(URL.createObjectURL(capturedFile));
            } else {
              setFile(capturedFile);
              setPreviewUrl(URL.createObjectURL(capturedFile));
            }
            stopCamera();
            setStep(2);
          }
        }, 'image/jpeg', 0.7);"""

content = content.replace(cap_old, cap_new)

# Add handleFile2Change if missing
handle_new = """  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
      setStep(2);
    }
  };

  const handleFile2Change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile2(selected);
      setPreviewUrl2(URL.createObjectURL(selected));
      setStep(2);
    }
  };"""

if "handleFile2Change" not in content:
    content = re.sub(r"  const handleFileChange = \(e: React.ChangeEvent<HTMLInputElement>\) => {[\s\S]*?  };", handle_new, content)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
