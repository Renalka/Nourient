import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. Add scanMode state
if "const [scanMode, setScanMode]" not in content:
    content = content.replace(
        "const [step, setStep] = useState<1|2|3|4>(1);",
        "const [step, setStep] = useState<1|2|3|4>(1);\n  const [scanMode, setScanMode] = useState<'ingredients' | 'front'>('ingredients');"
    )

# 2. Update processImage endpoint
old_endpoint_logic = """      const endpoint = isEnhanced 
        ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner' 
        : 'http://localhost:8003/api/v1/orchestrate/scanner';"""

new_endpoint_logic = """      const endpoint = scanMode === 'front'
        ? 'http://localhost:8003/api/v1/orchestrate/front-scanner'
        : (isEnhanced 
            ? 'http://localhost:8003/api/v1/orchestrate/enhanced_scanner' 
            : 'http://localhost:8003/api/v1/orchestrate/scanner');"""
            
content = content.replace(old_endpoint_logic, new_endpoint_logic)

# 3. Add UI selection in Step 1
step1_ui = """                  <ul className="space-y-4">
                    {["Front of the pack", "Ingredients list", "Nutrition facts", "Claims (optional)"].map((item, i) => (
                      <li key={i} className="flex items-center gap-3 text-sm text-gray-600 font-medium">
                        <div className="w-5 h-5 rounded-full bg-brand-light flex items-center justify-center text-brand">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                        </div>
                        {item}
                      </li>
                    ))}
                  </ul>"""

step1_ui_new = """                  <div className="mb-6">
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Select Scan Mode</label>
                    <div className="flex flex-col gap-3">
                      <button 
                        onClick={() => setScanMode('ingredients')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'ingredients' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'ingredients' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'ingredients' ? 'text-brand-dark' : 'text-gray-700'}`}>Ingredients Analysis</h3>
                            <p className="text-xs text-gray-500">Scan back-of-pack for UPF score & toxicity</p>
                          </div>
                        </div>
                      </button>
                      <button 
                        onClick={() => setScanMode('front')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'front' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'front' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'front' ? 'text-brand-dark' : 'text-gray-700'}`}>Front of Pack</h3>
                            <p className="text-xs text-gray-500">Detect health halos & marketing tricks</p>
                          </div>
                        </div>
                      </button>
                    </div>
                  </div>"""
                  
content = content.replace(step1_ui, step1_ui_new)

# 4. Add UI Results for Front mode in Step 4
result_ui_target = """               <div className="space-y-8">
                 {/* Top Summary */}"""

front_result_ui = """               <div className="space-y-8">
                 {scanMode === 'front' && result && (
                   <div className="space-y-6">
                     <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
                       <div>
                         <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">Health Halo Deception Index</h2>
                         <p className="text-sm text-gray-500">How misleading is the visual marketing?</p>
                       </div>
                       <div className="flex items-center justify-center w-16 h-16 rounded-full border-4 border-brand-light">
                         <span className="text-xl font-bold text-brand">{result.health_halo?.deception_index || 0}/100</span>
                       </div>
                     </div>
                     
                     {result.health_halo && (
                       <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Visual Analysis</h3>
                         <p className="text-sm text-gray-600 mb-4">{result.health_halo.reasoning}</p>
                         <div className="flex flex-wrap gap-2">
                           {result.health_halo.visual_cues?.map((cue: string, i: number) => (
                             <span key={i} className="text-[10px] font-bold uppercase tracking-widest bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full">{cue}</span>
                           ))}
                         </div>
                       </div>
                     )}

                     {result.target_audience && (
                       <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Target Audience Profiling</h3>
                         <p className="text-sm text-brand font-bold mb-4">Demographic: {result.target_audience.demographic}</p>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           <div>
                             <h4 className="text-[10px] text-gray-400 uppercase tracking-widest mb-2 font-bold">Marketing Indicators</h4>
                             <ul className="space-y-2">
                               {result.target_audience.indicators?.map((ind: string, i: number) => (
                                 <li key={i} className="text-xs text-gray-600 flex items-start gap-2">
                                   <span className="text-brand">•</span> {ind}
                                 </li>
                               ))}
                             </ul>
                           </div>
                           <div>
                             <h4 className="text-[10px] text-red-400 uppercase tracking-widest mb-2 font-bold">Health Concerns</h4>
                             <ul className="space-y-2">
                               {result.target_audience.concerns?.map((con: string, i: number) => (
                                 <li key={i} className="text-xs text-red-600 flex items-start gap-2">
                                   <span className="text-red-500">⚠</span> {con}
                                 </li>
                               ))}
                             </ul>
                           </div>
                         </div>
                       </div>
                     )}

                     {result.prominent_ingredients && result.prominent_ingredients.length > 0 && (
                       <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Prominent Ingredient Illusion</h3>
                         <div className="space-y-4">
                           {result.prominent_ingredients.map((ing: any, i: number) => (
                             <div key={i} className="p-4 bg-brand-light rounded-xl border border-brand/20">
                               <h4 className="font-bold text-sm text-brand-dark mb-1">{ing.name}</h4>
                               <p className="text-xs text-gray-600 mb-2"><span className="font-bold text-gray-500">Implied:</span> {ing.implied_quantity}</p>
                               <p className="text-xs text-gray-600"><span className="font-bold text-gray-500">Reality Check:</span> {ing.reality_check}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}
                     
                     <div className="flex justify-center mt-8">
                       <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                         Scan Another Image
                       </button>
                     </div>
                   </div>
                 )}

                 {scanMode === 'ingredients' && (
                   <>
"""

# Need to close the fragments for scanMode === 'ingredients'
result_ui_close_target = """                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
              </div>"""

result_ui_close_new = """                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
                 </>
                 )}
              </div>"""

content = content.replace(result_ui_target, front_result_ui + "                 {/* Top Summary */}")
content = content.replace(result_ui_close_target, result_ui_close_new)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

