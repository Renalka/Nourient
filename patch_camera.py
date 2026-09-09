import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. State changes
content = content.replace(
    "const [isCameraActive, setIsCameraActive] = useState(false);",
    "const [activeCameraSlot, setActiveCameraSlot] = useState<1 | 2 | null>(null);\n  const isCameraActive = activeCameraSlot !== null;"
)

# 2. Function changes
start_old = """  const startCamera = async () => {
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
    }
  };"""

start_new = """  const startCamera = async (slot: 1 | 2 = 1) => {
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
content = content.replace(start_old, start_new)

stop_old = """    }
    setIsCameraActive(false);
  };"""
stop_new = """    }
    setActiveCameraSlot(null);
  };"""
content = content.replace(stop_old, stop_new)

cap_old = """      canvas.toBlob((blob) => {
        if (blob) {
          const capturedFile = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
          setFile(capturedFile);
          setPreviewUrl(URL.createObjectURL(capturedFile));
          stopCamera();
        }
      }, 'image/jpeg');"""
cap_new = """      canvas.toBlob((blob) => {
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
content = content.replace(cap_old, cap_new)


# 3. Viewfinder UI changes
viewfinder_old = """                   <div className="flex flex-col gap-8 w-full items-center">
                     {scanMode === 'claims' ? (
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">"""

viewfinder_new = """                   <div className="flex flex-col gap-8 w-full items-center">
                     {isCameraActive ? (
                       <div className="flex flex-col items-center w-full">
                         <div className="relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 border-dashed border-brand flex items-center justify-center bg-gray-50 overflow-hidden cursor-pointer shadow-lg" onClick={capturePhoto}>
                           <div className="absolute top-4 z-10 bg-black/60 text-white px-4 py-1.5 rounded-full text-xs font-bold backdrop-blur-md">
                             {activeCameraSlot === 2 ? "Capturing Back (Ingredients)" : "Capturing Front of Pack"}
                           </div>
                           <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover block" />
                           <canvas ref={canvasRef} className="hidden" />
                           <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-brand"></div>
                           <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-brand"></div>
                           <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-brand"></div>
                           <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-brand"></div>
                         </div>
                       </div>
                     ) : scanMode === 'claims' ? (
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">"""

content = content.replace(viewfinder_old, viewfinder_new)

# Add Camera buttons to the empty states of Claims View
# Front empty state:
front_empty_old = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Upload Front</h3>
                               <p className="text-xs text-gray-500">Photo of marketing claims</p>
                             </div>"""

front_empty_new = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Front of Pack</h3>
                               <div className="flex gap-2 mt-3 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(1); }} className="px-3 py-1.5 bg-brand text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>"""

content = content.replace(front_empty_old, front_empty_new)

# Back empty state:
back_empty_old = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Upload Back</h3>
                               <p className="text-xs text-gray-500">Photo of ingredients list</p>
                             </div>"""

back_empty_new = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Back of Pack</h3>
                               <div className="flex gap-2 mt-3 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(2); }} className="px-3 py-1.5 bg-gray-800 text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef2.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>"""

content = content.replace(back_empty_old, back_empty_new)

# Remove the videoRef and canvasRef from the Single Box view since it's now handled at the top
single_box_old = """                     <div 
                       className="relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 border-dashed border-gray-300 flex items-center justify-center bg-gray-50 overflow-hidden cursor-pointer hover:bg-gray-100 transition-colors"
                       onClick={isCameraActive ? capturePhoto : (step === 1 ? startCamera : undefined)}
                     >
                        <video ref={videoRef} autoPlay playsInline className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`} />
                        <canvas ref={canvasRef} className="hidden" />
                        
                        {!isCameraActive && (
                          previewUrl ? ("""

single_box_new = """                     <div 
                       className="relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 border-dashed border-gray-300 flex items-center justify-center bg-gray-50 overflow-hidden cursor-pointer hover:bg-gray-100 transition-colors"
                       onClick={step === 1 ? () => startCamera(1) : undefined}
                     >
                        {previewUrl ? ("""
content = content.replace(single_box_old, single_box_new)

single_box_bot_old = """                          )
                        )}
                        
                        {/* Corner markers */}
                        <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-brand"></div>
                        <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-brand"></div>
                        <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-brand"></div>
                        <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-brand"></div>
                     </div>"""

single_box_bot_new = """                        ) : (
                          <div className="text-center">
                            <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400">
                              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                            </div>
                            <p className="text-sm font-medium text-gray-500">Tap to activate camera</p>
                          </div>
                        )}
                     </div>"""

# Ensure we don't accidentally replace the outer div
# I'll just use Regex to wipe out the redundant `!isCameraActive` block closure.
import re
content = re.sub(r"\n\s*\)\n\s*\)\}\n\s*\{\/\* Corner markers \*\/\}[\s\S]*?<\/div>", "\n" + single_box_bot_new, content, count=1)

# Now fix the Bottom Controls Button
bot_controls_old = """onClick={step === 1 ? (isCameraActive ? stopCamera : startCamera) : handleRetake}"""
bot_controls_new = """onClick={step === 1 ? (isCameraActive ? stopCamera : () => startCamera(1)) : handleRetake}"""
content = content.replace(bot_controls_old, bot_controls_new)

bot_controls_old2 = """onClick={step === 1 ? (isCameraActive ? capturePhoto : startCamera) : () => processImage(false)}"""
bot_controls_new2 = """onClick={step === 1 ? (isCameraActive ? capturePhoto : () => startCamera(1)) : () => processImage(false)}"""
content = content.replace(bot_controls_old2, bot_controls_new2)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
