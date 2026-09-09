import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Replace Viewfinder
old_viewfinder = """                   <div className="flex flex-col gap-8 w-full items-center">
                     {/* Main Frame */}
                     <div 
                       onClick={() => uploadInputRef.current?.click()}
                       className={`relative w-full max-w-sm aspect-[3/4] rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}
                     >
                       {previewUrl ? (
                         <>
                           <img src={previewUrl} alt="Product label" className="w-full h-full object-cover" />
                           <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                             <div className="bg-white text-gray-900 text-sm font-medium px-4 py-2 rounded-full">
                               Replace Image
                             </div>
                           </div>
                         </>
                       ) : (
                         <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                           <div className="w-16 h-16 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                             <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                           </div>
                           <h3 className="text-lg font-bold text-gray-900 mb-2">Capture Product Label</h3>
                           <p className="text-sm text-gray-500 mb-6 max-w-[200px]">Center the ingredients text clearly in the frame</p>
                           <div className="px-6 py-3 bg-brand text-white text-sm font-bold rounded-xl shadow-md shadow-brand/20">
                             Open Camera or Gallery
                           </div>
                         </div>
                       )}
                     </div>
                   </div>"""

new_viewfinder = """                   <div className="flex flex-col gap-8 w-full items-center">
                     {scanMode === 'claims' ? (
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
                         {/* Front Input */}
                         <div 
                           onClick={() => uploadInputRef.current?.click()}
                           className={`relative w-full aspect-square rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}
                         >
                           {previewUrl ? (
                             <>
                               <img src={previewUrl} alt="Front of pack" className="w-full h-full object-cover" />
                               <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                 <div className="bg-white text-gray-900 text-sm font-medium px-4 py-2 rounded-full">Replace Front</div>
                               </div>
                             </>
                           ) : (
                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Upload Front</h3>
                               <p className="text-xs text-gray-500">Photo of marketing claims</p>
                             </div>
                           )}
                         </div>

                         {/* Back Input */}
                         <div 
                           onClick={() => uploadInputRef2.current?.click()}
                           className={`relative w-full aspect-square rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl2 ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}
                         >
                           <input type="file" accept="image/*" ref={uploadInputRef2} onChange={handleFile2Change} className="hidden" />
                           {previewUrl2 ? (
                             <>
                               <img src={previewUrl2} alt="Back of pack" className="w-full h-full object-cover" />
                               <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                 <div className="bg-white text-gray-900 text-sm font-medium px-4 py-2 rounded-full">Replace Back</div>
                               </div>
                             </>
                           ) : (
                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Upload Back</h3>
                               <p className="text-xs text-gray-500">Photo of ingredients list</p>
                             </div>
                           )}
                         </div>
                       </div>
                     ) : (
                       {/* Main Frame */}
                       <div 
                         onClick={() => uploadInputRef.current?.click()}
                         className={`relative w-full max-w-sm aspect-[3/4] rounded-3xl border-2 overflow-hidden transition-all duration-300 cursor-pointer group ${previewUrl ? 'border-brand' : 'border-dashed border-gray-300 hover:border-brand/50 hover:bg-brand-light/10'}`}
                       >
                         {previewUrl ? (
                           <>
                             <img src={previewUrl} alt="Product label" className="w-full h-full object-cover" />
                             <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                               <div className="bg-white text-gray-900 text-sm font-medium px-4 py-2 rounded-full">
                                 Replace Image
                               </div>
                             </div>
                           </>
                         ) : (
                           <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                             <div className="w-16 h-16 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                               <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                             </div>
                             <h3 className="text-lg font-bold text-gray-900 mb-2">Capture Product Label</h3>
                             <p className="text-sm text-gray-500 mb-6 max-w-[200px]">Center the ingredients text clearly in the frame</p>
                             <div className="px-6 py-3 bg-brand text-white text-sm font-bold rounded-xl shadow-md shadow-brand/20">
                               Open Camera or Gallery
                             </div>
                           </div>
                         )}
                       </div>
                     )}
                   </div>"""

if "Main Frame" in content:
    content = content.replace(old_viewfinder, new_viewfinder)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
