import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

target = """                   <div className="flex flex-col gap-8 w-full items-center">
                     {/* Main Frame */}"""

new_code = """                   <div className="flex flex-col gap-8 w-full items-center">
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
                       <div className="flex flex-col items-center w-full">
                         {/* Main Frame */}"""

# We also need to close the `) : (` block. Where does it end?
action_target = """                     {/* Action Buttons */}"""
action_new = """                       </div>
                     )}
                     
                     {/* Action Buttons */}"""

if "Upload Front" not in content:
    content = content.replace(target, new_code)
    content = content.replace(action_target, action_new)
    
    # Also fix the unescaped entities ESLint complained about
    content = content.replace('Claim: "{c.claim}"', 'Claim: &quot;{c.claim}&quot;')
    content = content.replace('Claim: "{l.claim}"', 'Claim: &quot;{l.claim}&quot;')
    content = content.replace('"{b.word}"', '&quot;{b.word}&quot;')

    with open('frontend/src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
        print("Patched Viewfinder properly")
else:
    print("Already patched viewfinder")

