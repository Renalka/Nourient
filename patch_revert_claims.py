import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. State changes
state_old = "const [activeCameraSlot, setActiveCameraSlot] = useState<1 | 2 | null>(null);\n  const isCameraActive = activeCameraSlot !== null;"
state_new = "const [isCameraActive, setIsCameraActive] = useState(false);\n  const [activeClaimsTab, setActiveClaimsTab] = useState<'front' | 'back'>('front');"
content = content.replace(state_old, state_new)

# 2. handleFileChange route
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
        if (scanMode === 'claims' && !file2) {
          setActiveClaimsTab('back');
        }
      }
    }
  };"""
content = content.replace(filechange_old, filechange_new)

# 3. startCamera, stopCamera, capturePhoto
start_old = """  const startCamera = async (slot: 1 | 2 = 1) => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      setActiveCameraSlot(slot);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Camera error:", err);
      alert("Could not access camera. Please check permissions or use the upload button.");
      setActiveCameraSlot(null);
    }
  };"""

start_new = """  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      setIsCameraActive(true);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Camera error:", err);
      alert("Could not access camera. Please check permissions or use the upload button.");
      setIsCameraActive(false);
    }
  };"""
content = content.replace(start_old, start_new)

stop_old = """    }
    setActiveCameraSlot(null);
  };"""
stop_new = """    }
    setIsCameraActive(false);
  };"""
content = content.replace(stop_old, stop_new)

cap_old = """      canvas.toBlob((blob) => {
        if (blob) {
          const capturedFile = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
          if (activeCameraSlot === 2) {
            setFile2(capturedFile);
            setPreviewUrl2(URL.createObjectURL(capturedFile));
          } else {
            setFile(capturedFile);
            setPreviewUrl(URL.createObjectURL(capturedFile));
          }
          stopCamera();
        }
      }, 'image/jpeg');"""

cap_new = """      canvas.toBlob((blob) => {
        if (blob) {
          const capturedFile = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
          if (scanMode === 'claims' && activeClaimsTab === 'back') {
            setFile2(capturedFile);
            setPreviewUrl2(URL.createObjectURL(capturedFile));
          } else {
            setFile(capturedFile);
            setPreviewUrl(URL.createObjectURL(capturedFile));
            if (scanMode === 'claims' && !file2) {
              setActiveClaimsTab('back');
            }
          }
          stopCamera();
        }
      }, 'image/jpeg');"""
content = content.replace(cap_old, cap_new)

# 4. Viewfinder replacement
start_idx = content.find('<div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">')
end_idx = content.find('          )}', start_idx) + 12

new_viewfinder = """<div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef}
                     onChange={handleFileChange}
                     className="hidden"
                   />
                   
                   <div className="flex flex-col gap-8 w-full items-center">
                     <div className="flex flex-col items-center w-full">
                       {/* Single Main Frame */}
                       <div 
                         className={`relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 overflow-hidden cursor-pointer transition-colors flex items-center justify-center ${isCameraActive ? 'border-brand bg-gray-50 shadow-lg' : 'border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100'}`}
                         onClick={isCameraActive ? capturePhoto : (step === 1 ? startCamera : undefined)}
                       >
                          {scanMode === 'claims' && isCameraActive && (
                            <div className="absolute top-4 z-10 bg-black/60 text-white px-4 py-1.5 rounded-full text-xs font-bold backdrop-blur-md">
                              {activeClaimsTab === 'back' ? "Capturing Back (Ingredients)" : "Capturing Front of Pack"}
                            </div>
                          )}
                          <video ref={videoRef} autoPlay playsInline className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`} />
                          <canvas ref={canvasRef} className="hidden" />
                          
                          {!isCameraActive && (
                            (scanMode === 'claims' && activeClaimsTab === 'back' ? previewUrl2 : previewUrl) ? (
                              <img src={scanMode === 'claims' && activeClaimsTab === 'back' ? previewUrl2! : previewUrl!} alt="Preview" className="w-full h-full object-cover" />
                            ) : (
                              <div className="text-center p-6">
                                <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400">
                                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                                </div>
                                <h3 className="text-sm font-bold text-gray-900 mb-1">
                                  {scanMode === 'claims' ? (activeClaimsTab === 'back' ? "Back of Pack" : "Front of Pack") : "Capture Product Label"}
                                </h3>
                                <p className="text-xs text-gray-500">Tap to activate camera</p>
                              </div>
                            )
                          )}
                          
                          {/* Corner markers */}
                          <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-brand"></div>
                          <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-brand"></div>
                          <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-brand"></div>
                          <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-brand"></div>
                       </div>

                       {/* Thumbnails Row */}
                       <div className="flex flex-row gap-6 justify-center mt-8">
                          {scanMode === 'claims' ? (
                            <>
                              <div className="space-y-2 text-center cursor-pointer" onClick={() => setActiveClaimsTab('front')}>
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${activeClaimsTab === 'front' ? 'border-brand' : (previewUrl ? 'border-brand border-solid' : 'border-gray-200 border-dashed')} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors relative`}>
                                  {previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                  {previewUrl && activeClaimsTab !== 'front' && <div className="absolute inset-0 bg-black/20"></div>}
                                </div>
                                <span className={`text-[11px] font-semibold ${activeClaimsTab === 'front' ? 'text-brand' : 'text-gray-500'}`}>Front Pack</span>
                              </div>
                              <div className="space-y-2 text-center cursor-pointer" onClick={() => setActiveClaimsTab('back')}>
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${activeClaimsTab === 'back' ? 'border-brand' : (previewUrl2 ? 'border-brand border-solid' : 'border-gray-200 border-dashed')} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors relative`}>
                                  {previewUrl2 ? <img src={previewUrl2} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                  {previewUrl2 && activeClaimsTab !== 'back' && <div className="absolute inset-0 bg-black/20"></div>}
                                </div>
                                <span className={`text-[11px] font-semibold ${activeClaimsTab === 'back' ? 'text-brand' : 'text-gray-500'}`}>Ingredients</span>
                              </div>
                            </>
                          ) : (
                            ["Front", "Ingredients", "Nutrition"].map((label, i) => (
                              <div key={i} className="space-y-2 text-center">
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${i===0 && previewUrl ? 'border-brand' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                                  {i===0 && previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                </div>
                                <span className="text-[11px] font-semibold text-gray-500">{label}</span>
                              </div>
                            ))
                          )}
                       </div>
                     </div>
                   </div>

                   {/* Bottom Controls */}
                   <div className="flex justify-center items-center gap-4 mt-4 pt-4 border-t border-gray-100 w-full flex-wrap">
                     <button onClick={step === 1 ? (isCameraActive ? stopCamera : handleRetake) : handleRetake} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-28 text-center">
                       {step === 1 ? (isCameraActive ? 'Cancel' : 'Retake') : 'Retake'}
                     </button>
                     
                     <div 
                        onClick={step === 1 ? (isCameraActive ? capturePhoto : startCamera) : () => processImage(false)}
                        className={`w-16 h-16 rounded-full border-4 border-gray-200 flex items-center justify-center cursor-pointer hover:border-brand transition-colors ${step === 2 ? 'hidden' : ''}`}
                      >
                       <div className={`w-12 h-12 rounded-full shadow-md ${isCameraActive ? 'bg-red-500' : 'bg-brand'}`}></div>
                     </div>
                     
                     <button onClick={step === 1 ? () => uploadInputRef.current?.click() : () => processImage(false)} className={`px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm ${step === 2 ? 'w-32 bg-gray-100' : 'w-28'}`}>
                       {step === 1 ? 'Upload' : (addingToBasket ? 'Loading...' : (basketMsg ? basketMsg : 'Analyze'))}
                     </button>
                   </div>
                </div>
              </div>
          )}
"""

content = content[:start_idx] + new_viewfinder + content[end_idx:]

# Remove unused uploadInputRef2
content = content.replace("  const uploadInputRef2 = useRef<HTMLInputElement>(null);\n", "")

# Remove handleFile2Change
file2_block = """  const handleFile2Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile2(selectedFile);
      const url = URL.createObjectURL(selectedFile);
      setPreviewUrl2(url);
    }
  };\n"""
content = content.replace(file2_block, "")

# Remove previewUrl2 reset in handleRetake
retake_old = """  const handleRetake = () => {
    setStep(1);
    setFile(null);
    setPreviewUrl(null);
    setFile2(null);
    setPreviewUrl2(null);
    setResult(null);
  };"""
retake_new = """  const handleRetake = () => {
    setStep(1);
    setFile(null);
    setPreviewUrl(null);
    setFile2(null);
    setPreviewUrl2(null);
    setActiveClaimsTab('front');
    setResult(null);
  };"""
content = content.replace(retake_old, retake_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

