import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. Patch capturePhoto
cap_old = """        canvas.toBlob((blob) => {
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

cap_new = """        canvas.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
            if (scanMode === 'claims') {
              if (activeClaimsTab === 'back') {
                setFile2(capturedFile);
                setPreviewUrl2(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file) setStep(2);
              } else {
                setFile(capturedFile);
                setPreviewUrl(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file2) setStep(2);
                else setActiveClaimsTab('back'); // Auto-advance tab!
              }
            } else {
              setFile(capturedFile);
              setPreviewUrl(URL.createObjectURL(capturedFile));
              stopCamera();
              setStep(2);
            }
          }
        }, 'image/jpeg', 0.7);"""
content = content.replace(cap_old, cap_new)

# 2. Patch handleFileChange
handle1_old = """  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile(compressed);
      setPreviewUrl(URL.createObjectURL(compressed));
      setStep(2);
    }
  };"""

handle1_new = """  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile(compressed);
      setPreviewUrl(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file2) setStep(2);
        else setActiveClaimsTab('back');
      } else {
        setStep(2);
      }
    }
  };"""
content = content.replace(handle1_old, handle1_new)

# 3. Patch handleFile2Change
handle2_old = """  const handleFile2Change = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      setStep(2);
    }
  };"""

handle2_new = """  const handleFile2Change = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file) setStep(2);
      } else {
        setStep(2);
      }
    }
  };"""
content = content.replace(handle2_old, handle2_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
