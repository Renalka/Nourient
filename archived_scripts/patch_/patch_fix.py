import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

nutr_render = """
                 {scanMode === 'nutrition' && result && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Product analysis header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           <h1 className="text-3xl font-serif mb-1 drop-shadow-md">Nutrition Panel Analysis</h1>
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Portion Loopholes • Macro Quality</p>
                         </div>
                       </div>
                     </div>

                     {/* Core Metrics Grid */}
                     <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Realistic Serving Size */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" /></svg>
                            Realistic Serving
                          </h2>
                          <div className="relative z-10">
                            <div className="flex items-baseline gap-2 mb-2">
                              <p className={`text-4xl font-serif leading-none ${result.analyzed_serving?.is_loophole ? 'text-red-600' : 'text-brand'}`}>
                                {result.analyzed_serving?.realistic_amount}
                              </p>
                              <span className="text-lg font-bold text-gray-400">{result.analyzed_serving?.unit}</span>
                            </div>
                            {result.analyzed_serving?.is_loophole ? (
                              <span className="inline-block bg-red-100 text-red-700 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Loophole Exposer: {result.analyzed_serving?.multiplier}x Multiplier</span>
                            ) : (
                              <span className="inline-block bg-brand-light text-brand text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Honest Portion</span>
                            )}
                          </div>
                        </div>

                        {/* Empty Calorie Ratio */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" /></svg>
                            Empty Calorie Ratio
                          </h2>
                          <div className="flex items-end justify-between relative z-10">
                            <div>
                              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-lg font-black text-white shadow-md mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3 ${(result.empty_calorie_ratio?.ratio || 0) > 0.4 ? 'bg-red-500' : 'bg-green-500'}`}>
                                {Math.round((result.empty_calorie_ratio?.ratio || 0) * 100)}%
                              </div>
                              <p className="text-3xl font-serif text-foreground leading-none">{result.empty_calorie_ratio?.empty_calories}</p>
                              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">Empty Cals / 100g</p>
                            </div>
                          </div>
                        </div>

                        {/* Threshold Warnings Count */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                            Threshold Flags
                          </h2>
                          <div className="relative z-10">
                            <p className={`text-4xl font-serif leading-none mb-2 ${result.threshold_warnings?.length > 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {result.threshold_warnings?.length || 0}
                            </p>
                            <span className={`inline-block text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full ${result.threshold_warnings?.length > 0 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                              {result.threshold_warnings?.length > 0 ? 'High Daily Value' : 'Within Limits'}
                            </span>
                          </div>
                        </div>
                     </div>

                     {/* Detailed Insight Columns */}
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       
                       {/* Left Column: Serving Loophole */}
                       <div className="space-y-6">
                         {result.analyzed_serving && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                               Serving Size Exposer
                             </h2>
                             {result.analyzed_serving.is_loophole ? (
                               <div className="p-4 rounded-xl border-l-4 border-red-500 bg-red-50 mb-4">
                                 <p className="text-sm text-red-800 leading-relaxed font-medium">{result.analyzed_serving.loophole_warning}</p>
                               </div>
                             ) : (
                               <div className="p-4 rounded-xl border-l-4 border-green-500 bg-green-50 mb-4">
                                 <p className="text-sm text-green-800 leading-relaxed font-medium">The stated serving size of {result.stated_serving?.amount}{result.stated_serving?.unit} is realistic.</p>
                               </div>
                             )}
                             <div className="mt-4 pt-4 border-t border-gray-100">
                               <p className="text-xs text-gray-500 mb-1">Stated vs Realistic Comparison:</p>
                               <div className="flex items-center gap-4">
                                 <div className="text-center bg-gray-50 p-2 rounded-lg flex-1">
                                    <span className="block text-[10px] uppercase font-bold text-gray-400">Label Claims</span>
                                    <span className="font-bold text-brand-dark">{result.stated_serving?.amount}{result.stated_serving?.unit}</span>
                                 </div>
                                 <div className="text-gray-300">➜</div>
                                 <div className="text-center bg-brand-light p-2 rounded-lg flex-1">
                                    <span className="block text-[10px] uppercase font-bold text-brand">Actual Portion</span>
                                    <span className="font-bold text-brand">{result.analyzed_serving.realistic_amount}{result.analyzed_serving.unit}</span>
                                 </div>
                               </div>
                             </div>
                           </div>
                         )}
                       </div>

                       {/* Right Column: Threshold Warnings */}
                       <div className="space-y-6">
                         {result.threshold_warnings && result.threshold_warnings.length > 0 ? (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center justify-between">
                               Acceptable Daily Intake (ADI)
                               <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Over Limit</span>
                             </h2>
                             <div className="space-y-3">
                               {result.threshold_warnings.map((warn: any, i: number) => (
                                 <div key={i} className="flex flex-col p-4 bg-red-50/50 rounded-xl border border-red-100 gap-2">
                                   <div className="flex items-center justify-between">
                                     <span className="font-bold text-sm text-red-700">{warn.nutrient}</span>
                                     <span className="text-[10px] uppercase font-bold text-red-600 tracking-widest bg-red-100 px-2 py-1 rounded-full">{warn.percentage_of_adi}% of Daily Limit</span>
                                   </div>
                                   <p className="text-xs text-red-700 leading-relaxed">{warn.warning_message}</p>
                                   <div className="w-full bg-red-100 rounded-full h-1.5 mt-1">
                                     <div className="bg-red-500 h-1.5 rounded-full" style={{width: `${Math.min(100, warn.percentage_of_adi)}%`}}></div>
                                   </div>
                                 </div>
                               ))}
                             </div>
                           </div>
                         ) : (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-center h-full min-h-[200px]">
                              <div className="text-center">
                                <div className="w-12 h-12 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                </div>
                                <p className="text-sm font-bold text-green-700">No Macro Thresholds Exceeded</p>
                                <p className="text-xs text-gray-500 mt-1">This product is within safe daily limits.</p>
                              </div>
                           </div>
                         )}
                       </div>
                     </div>
                   </div>
                 )}
"""

if "Nutrition Panel Analysis" not in content:
    inject_target = "                 {scanMode === 'front' && ("
    content = content.replace(inject_target, nutr_render + "\n\n" + inject_target)
    with open('frontend/src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
        print("Patched successfully")
else:
    print("Already patched")

