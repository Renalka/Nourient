import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_code = """                          ) : (
                            ["Front", "Ingredients", "Nutrition"].map((label, i) => (
                              <div key={i} className="space-y-2 text-center">
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${i===0 && previewUrl ? 'border-brand' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                                  {i===0 && previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                </div>
                                <span className="text-[11px] font-semibold text-gray-500">{label}</span>
                              </div>
                            ))
                          )}"""

new_code = """                          ) : (
                            <div className="space-y-2 text-center">
                              <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${previewUrl ? 'border-brand border-solid' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                                {previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                              </div>
                              <span className="text-[11px] font-semibold text-gray-500">
                                {scanMode === 'ingredients' ? 'Ingredients Label' : 
                                 scanMode === 'nutrition' ? 'Nutrition Facts' : 
                                 scanMode === 'front' ? 'Front of Pack' : 'Captured Image'}
                              </span>
                            </div>
                          )}"""

content = content.replace(old_code, new_code)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
