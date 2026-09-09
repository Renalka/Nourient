import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Replace Front Empty State
front_empty_old = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-brand-light/30 text-brand rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Front of Pack</h3>
                               <p className="text-xs text-gray-500 mb-3">Photo of marketing claims</p>
                               <div className="flex gap-2 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(1); }} className="px-3 py-1.5 bg-brand text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>"""

front_empty_new = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center" onClick={(e) => { e.stopPropagation(); startCamera(1); }}>
                               <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400 group-hover:bg-brand-light/20 transition-colors">
                                 <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Front of Pack</h3>
                               <p className="text-xs font-medium text-gray-500 mb-4">Tap to activate camera</p>
                               <button onClick={(e) => { e.stopPropagation(); uploadInputRef.current?.click(); }} className="text-[10px] uppercase tracking-widest font-bold text-brand hover:underline relative z-10">
                                 Or Upload File
                               </button>
                             </div>"""

# Replace Back Empty State
back_empty_old = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                               <div className="w-12 h-12 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Back of Pack</h3>
                               <p className="text-xs text-gray-500 mb-3">Photo of ingredients</p>
                               <div className="flex gap-2 relative z-10">
                                 <button onClick={(e) => { e.stopPropagation(); startCamera(2); }} className="px-3 py-1.5 bg-gray-800 text-white rounded-lg text-xs font-bold shadow-md">Camera</button>
                                 <button onClick={(e) => { e.stopPropagation(); uploadInputRef2.current?.click(); }} className="px-3 py-1.5 bg-white text-gray-700 border border-gray-200 rounded-lg text-xs font-bold shadow-sm">Upload</button>
                               </div>
                             </div>"""

back_empty_new = """                             <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center" onClick={(e) => { e.stopPropagation(); startCamera(2); }}>
                               <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400 group-hover:bg-brand-light/20 transition-colors">
                                 <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                               </div>
                               <h3 className="text-sm font-bold text-gray-900 mb-1">Back of Pack</h3>
                               <p className="text-xs font-medium text-gray-500 mb-4">Tap to activate camera</p>
                               <button onClick={(e) => { e.stopPropagation(); uploadInputRef2.current?.click(); }} className="text-[10px] uppercase tracking-widest font-bold text-brand hover:underline relative z-10">
                                 Or Upload File
                               </button>
                             </div>"""

content = content.replace(front_empty_old, front_empty_new)
content = content.replace(back_empty_old, back_empty_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

print("Empty states patched")

