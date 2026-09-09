import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Locate the beginning of Step 4
target = """            {step === 4 && result && (
              <div className="space-y-8 animate-fade-in pb-12">
                 {/* Hero Header */}"""

# We want to conditionally render the normal ingredient results OR the new Front of Pack results based on `scanMode`

replacement = """            {step === 4 && result && (
              <div className="space-y-8 animate-fade-in pb-12">
                 {scanMode === 'front' && (
                   <div className="space-y-6">
                     <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
                       <div>
                         <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">Health Halo Deception Index</h2>
                         <p className="text-sm text-gray-500">How misleading is the visual marketing?</p>
                       </div>
                       <div className="flex items-center justify-center w-16 h-16 rounded-full border-4 border-brand-light bg-brand/5">
                         <span className="text-xl font-bold text-brand">{result.health_halo?.deception_index || 0}</span><span className="text-xs text-gray-400">/100</span>
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
                   </div>
                 )}

                 {scanMode === 'ingredients' && (
                   <>
                 {/* Hero Header */}"""

content = content.replace(target, replacement)

target_close = """                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
              </div>"""

replacement_close = """                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
                 </>
                 )}

                 {scanMode === 'front' && (
                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Image
                   </button>
                 </div>
                 )}
              </div>"""

content = content.replace(target_close, replacement_close)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

