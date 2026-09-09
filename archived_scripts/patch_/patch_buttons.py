import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Replace the middle Upload/Analyze button
old_middle_btn = """                     <button onClick={step === 1 ? () => (scanMode === 'claims' && activeClaimsTab === 'back' ? uploadInputRef2.current?.click() : uploadInputRef.current?.click()) : () => processImage(false)} className={`px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm ${step === 2 ? 'w-32 bg-gray-100' : 'w-28'}`}>
                       {step === 1 ? 'Upload' : (addingToBasket ? 'Loading...' : (basketMsg ? basketMsg : 'Analyze'))}
                     </button>"""

new_middle_btn = """                     {step === 1 && (
                       <button onClick={() => (scanMode === 'claims' && activeClaimsTab === 'back' ? uploadInputRef2.current?.click() : uploadInputRef.current?.click())} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-28">
                         Upload
                       </button>
                     )}"""

content = content.replace(old_middle_btn, new_middle_btn)

# Replace the Deep Scan button
old_deep_btn = """                     {step === 2 && (
                       <button onClick={() => processImage(true)} className="px-4 py-2 bg-brand border border-brand rounded-full text-xs font-bold text-white hover:bg-brand-dark transition-colors shadow-sm w-32 flex items-center justify-center gap-2">
                         <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                         Deep Scan
                       </button>
                     )}"""

new_deep_btn = """                     {step === 2 && (
                       <button onClick={() => processImage(true)} className="px-4 py-2 bg-brand border border-brand rounded-full text-xs font-bold text-white hover:bg-brand-dark transition-colors shadow-sm w-32 flex items-center justify-center gap-2">
                         <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                         Scan
                       </button>
                     )}"""

content = content.replace(old_deep_btn, new_deep_btn)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

print("Patched buttons successfully.")
