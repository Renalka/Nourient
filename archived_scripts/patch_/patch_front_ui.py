import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Pattern to find the existing scanMode === 'front' block
# It starts with "{scanMode === 'front' && (" and ends right before "{scanMode === 'ingredients' && ("
pattern = r"\{scanMode === 'front' && \(\s*<div className=\"space-y-6\">.*?</div>\s*\)\}"

new_ui = """{scanMode === 'front' && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Product analysis header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           <h1 className="text-3xl font-serif mb-1 drop-shadow-md">Visual Packaging Analysis</h1>
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Front of Pack • Marketing & Deception</p>
                         </div>
                       </div>
                     </div>

                     {/* Core Metrics Grid */}
                     <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Deception Index */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                            Health Halo Deception
                          </h2>
                          <div className="flex items-end justify-between relative z-10">
                            <div>
                              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-xl font-black text-white shadow-md mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3 ${(result.health_halo?.deception_index || 0) > 70 ? 'bg-red-500' : ((result.health_halo?.deception_index || 0) > 40 ? 'bg-yellow-500' : 'bg-green-500')}`}>
                                {(result.health_halo?.deception_index || 0) > 70 ? 'HIGH' : ((result.health_halo?.deception_index || 0) > 40 ? 'MOD' : 'LOW')}
                              </div>
                              <p className="text-3xl font-serif text-foreground leading-none">{result.health_halo?.deception_index || 0}</p>
                              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">/ 100 Index</p>
                            </div>
                          </div>
                        </div>

                        {/* Target Audience */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                            Primary Demographic
                          </h2>
                          <div className="relative z-10">
                            <p className="text-xl font-bold text-foreground leading-tight mb-2">{result.target_audience?.demographic || 'General'}</p>
                            <span className="inline-block bg-brand-light text-brand text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Target Detected</span>
                          </div>
                        </div>

                        {/* Visual Vibe */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                            Visual Cues
                          </h2>
                          <div className="relative z-10 flex flex-wrap gap-2">
                             {result.health_halo?.visual_cues?.slice(0, 3).map((cue: string, i: number) => (
                               <span key={i} className="text-[9px] font-bold uppercase tracking-widest bg-gray-100 text-gray-600 px-2 py-1 rounded-md">{cue}</span>
                             ))}
                          </div>
                        </div>
                     </div>

                     {/* Main Insights Columns */}
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       
                       {/* Left Column: Visual Analysis */}
                       <div className="space-y-6">
                         {result.health_halo && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                               Health Halo Breakdown
                             </h2>
                             <div className="p-4 rounded-xl border-l-4 border-yellow-500 bg-yellow-50 mb-4">
                               <p className="text-sm text-yellow-800 leading-relaxed font-medium">{result.health_halo.reasoning}</p>
                             </div>
                           </div>
                         )}
                       </div>

                       {/* Right Column: Audience Concerns & Prominent Ingredients */}
                       <div className="space-y-6">
                         {result.target_audience?.concerns && result.target_audience.concerns.length > 0 && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center justify-between">
                               Audience Concerns
                               <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Flagged</span>
                             </h2>
                             <div className="space-y-3">
                               {result.target_audience.concerns.map((con: string, i: number) => (
                                 <div key={i} className="flex items-start gap-3 p-3 bg-red-50/50 rounded-xl border border-red-100">
                                   <span className="text-red-500 mt-0.5">⚠</span>
                                   <p className="text-xs text-red-700 leading-relaxed">{con}</p>
                                 </div>
                               ))}
                             </div>
                           </div>
                         )}
                         
                         {result.prominent_ingredients && result.prominent_ingredients.length > 0 && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4">Ingredient Illusions</h2>
                             <div className="space-y-3">
                               {result.prominent_ingredients.map((ing: any, i: number) => (
                                 <div key={i} className="flex flex-col p-4 bg-white rounded-xl border border-gray-100 shadow-sm gap-2">
                                   <div className="flex items-center justify-between border-b border-gray-50 pb-2">
                                     <span className="font-bold text-sm text-foreground">{ing.name}</span>
                                     <span className="text-[9px] uppercase font-bold text-brand tracking-widest bg-brand-light px-2 py-1 rounded-full">Front Tag</span>
                                   </div>
                                   <div className="text-xs text-gray-600 mt-1">
                                     <span className="font-bold text-gray-400 uppercase text-[9px] tracking-widest block mb-1">Marketing Implication</span>
                                     {ing.implied_quantity}
                                   </div>
                                   <div className="text-xs text-gray-600 mt-2 p-2 bg-gray-50 rounded-lg">
                                     <span className="font-bold text-gray-400 uppercase text-[9px] tracking-widest block mb-1">Reality Check</span>
                                     {ing.reality_check}
                                   </div>
                                 </div>
                               ))}
                             </div>
                           </div>
                         )}
                       </div>
                     </div>
                   </div>
                 )}"""

if "{scanMode === 'front' && (" in content:
    # Do a manual split/replace since regex with dots spanning multiple lines can be tricky
    start_idx = content.find("{scanMode === 'front' && (")
    end_idx = content.find("{scanMode === 'ingredients' && (")
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + new_ui + "\n\n                 " + content[end_idx:]
        with open('frontend/src/app/scanner/page.tsx', 'w') as f:
            f.write(new_content)
        print("Patched successfully")
    else:
        print("Could not find boundaries")
else:
    print("Could not find start pattern")
