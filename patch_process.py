import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_process = """  const processImage = async (isEnhanced = false) => {
    if (!file) return;
    setStep(3); // Analyzing
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = await getToken();

      const endpoint = scanMode === 'front'
        ? 'http://localhost:8003/api/v1/orchestrate/front-scanner'
        : scanMode === 'nutrition'
            ? 'http://localhost:8003/api/v1/orchestrate/nutrition-scanner'
            : (isEnhanced 
                ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner' 
                : 'http://localhost:8003/api/v1/orchestrate/scanner');"""

new_process = """  const processImage = async (isEnhanced = false) => {
    if (!file) return;
    if (scanMode === 'claims' && !file2) {
      setError("Please capture both the front and back of the pack to verify claims.");
      return;
    }
    setStep(3); // Analyzing
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    if (scanMode === 'claims' && file2) {
      formData.append('file2', file2);
    }

    try {
      const token = await getToken();

      const endpoint = scanMode === 'claims'
        ? 'http://localhost:8003/api/v1/orchestrate/claims-scanner'
        : scanMode === 'front'
        ? 'http://localhost:8003/api/v1/orchestrate/front-scanner'
        : scanMode === 'nutrition'
            ? 'http://localhost:8003/api/v1/orchestrate/nutrition-scanner'
            : (isEnhanced 
                ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner' 
                : 'http://localhost:8003/api/v1/orchestrate/scanner');"""

content = content.replace(old_process, new_process)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

