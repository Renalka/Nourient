import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

cap_old = """              if (activeClaimsTab === 'back') {
                setFile2(capturedFile);
                setPreviewUrl2(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file) setStep(2);
              } else {"""

cap_new = """              if (activeClaimsTab === 'back') {
                setFile2(capturedFile);
                setPreviewUrl2(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file) setStep(2);
                else setActiveClaimsTab('front');
              } else {"""
content = content.replace(cap_old, cap_new)

handle2_old = """      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file) setStep(2);
      } else {"""

handle2_new = """      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file) setStep(2);
        else setActiveClaimsTab('front');
      } else {"""
content = content.replace(handle2_old, handle2_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
