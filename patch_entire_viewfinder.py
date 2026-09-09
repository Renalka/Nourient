import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

start_idx = content.find('<div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">')

if start_idx == -1:
    print("Could not find start idx")
    exit(1)

end_target = "            {step === 3 && ("
end_idx = content.find(end_target)
if end_idx == -1:
    print("Could not find Step 3")
    exit(1)

new_viewfinder = """<div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef}
                     onChange={handleFileChange}
                     className="hidden"
                   />
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef2}
                     onChange={handleFile2Change}
                     className="hidden"
                   />
                   
                   <div className="flex flex-col gap-8 w-full items-center">
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
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
                         {/* Front Input */}
                         <div className={`relative w-full aspect-square rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}>
                           {previewUrl ? (
                             <>
                               <img src={previewUrl} alt="Front of pack" className="w-full h-full object-cover" />
                               <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-3">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(1); }} className="px-4 py-2 bg-white text-gray-900 text-sm font-bold rounded-full shadow-md">📷 Retake</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef.current?.click(); }} className="px-4 py-2 bg-brand text-white text-sm font-bold rounded-full shadow-md">📁 Upload</button>
                               </div>
                             </>
                           ) : (
                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Front of Pack</h3>
                               <p className="text-xs text-gray-500 mb-3">Photo of marketing claims</p>
                               <div className="flex gap-2 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(1); }} className="px-3 py-1.5 bg-brand text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>
                           )}
                         </div>

                         {/* Back Input */}
                         <div className={`relative w-full aspect-square rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl2 ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}>
                           {previewUrl2 ? (
                             <>
                               <img src={previewUrl2} alt="Back of pack" className="w-full h-full object-cover" />
                               <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-3">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(2); }} className="px-4 py-2 bg-white text-gray-900 text-sm font-bold rounded-full shadow-md">📷 Retake</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef2.current?.click(); }} className="px-4 py-2 bg-brand text-white text-sm font-bold rounded-full shadow-md">📁 Upload</button>
                               </div>
                             </>
                           ) : (
                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Back of Pack</h3>
                               <p className="text-xs text-gray-500 mb-3">Photo of ingredients</p>
                               <div className="flex gap-2 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(2); }} className="px-3 py-1.5 bg-gray-800 text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef2.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>
                           )}
                         </div>
                       </div>
                     ) : (
                       <div className="flex flex-col items-center w-full">
                         {/* Single Main Frame */}
                         <div 
                           className="relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 border-dashed border-gray-300 flex items-center justify-center bg-gray-50 overflow-hidden cursor-pointer hover:bg-gray-100 transition-colors"
                           onClick={step === 1 ? () => startCamera(1) : undefined}
                         >
                            {previewUrl ? (
                              <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                            ) : (
                              <div className="text-center">
                                <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400">
                                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                                </div>
                                <p className="text-sm font-medium text-gray-500">Tap to activate camera</p>
                              </div>
                            )}
                         </div>

                         {/* Thumbnails Row */}
                         <div className="flex flex-row gap-6 justify-center mt-8">
                            {["Front", "Ingredients", "Nutrition"].map((label, i) => (
                              <div key={i} className="space-y-2 text-center">
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${i===0 && previewUrl ? 'border-brand' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                                  {i===0 && previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                </div>
                                <span className="text-[11px] font-semibold text-gray-500">{label}</span>
                              </div>
                            ))}
                            <div className="space-y-2 text-center cursor-pointer">
                              <div className="w-16 h-16 mx-auto rounded-xl border border-gray-200 bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 transition-colors">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                              </div>
                              <span className="text-[11px] font-semibold text-gray-500">Add claims</span>
                            </div>
                         </div>
                       </div>
                     )}
                   </div>

                   {/* Bottom Controls */}
                   <div className="flex justify-center items-center gap-4 mt-4 pt-4 border-t border-gray-100 w-full flex-wrap">
                     <button onClick={step === 1 ? (isCameraActive ? stopCamera : handleRetake) : handleRetake} className={`px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-28 text-center ${!isCameraActive && scanMode === 'claims' ? 'hidden' : ''}`}>
                       {step === 1 ? (isCameraActive ? 'Cancel' : 'Retake') : 'Retake'}
                     </button>
                     
                     <div 
                        onClick={step === 1 ? (isCameraActive ? capturePhoto : () => startCamera(1)) : () => processImage(false)}
                        className={`w-16 h-16 rounded-full border-4 border-gray-200 flex items-center justify-center cursor-pointer hover:border-brand transition-colors ${step === 2 || (!isCameraActive && scanMode === 'claims') ? 'hidden' : ''}`}
                      >
                       <div className={`w-12 h-12 rounded-full shadow-md ${isCameraActive ? 'bg-red-500' : 'bg-brand'}`}></div>
                     </div>
                     
                     <button onClick={step === 1 ? () => uploadInputRef.current?.click() : () => processImage(false)} className={`px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm ${!isCameraActive && scanMode === 'claims' ? 'hidden' : ''} ${step === 2 ? 'w-32 bg-gray-100' : 'w-28'}`}>
                       {step === 1 ? 'Upload' : (addingToBasket ? 'Loading...' : (basketMsg ? basketMsg : 'Analyze'))}
                     </button>
                   </div>
                   
                   {scanMode === 'claims' && !isCameraActive && step === 1 && (
                     <div className="flex justify-center mt-4 w-full">
                       <button onClick={() => processImage(false)} className="px-8 py-3 bg-brand text-white rounded-full text-sm font-bold shadow-md hover:bg-brand-dark transition-colors">
                         {addingToBasket ? 'Loading...' : (basketMsg ? basketMsg : 'Analyze Claims')}
                       </button>
                     </div>
                   )}
                </div>
              </div>
            )}
\n"""

new_content = content[:start_idx] + new_viewfinder + content[end_idx:]
with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(new_content)
print("Replaced entire viewfinder successfully.")

