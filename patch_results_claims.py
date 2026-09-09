import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

claims_render = """
                 {scanMode === 'claims' && result && result.verification && (
                   <div className="space-y-8 animate-fade-in pb-12">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Claims verifier header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           <h1 className="text-3xl font-serif mb-1 drop-shadow-md">Claims Verifier</h1>
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Marketing vs Reality</p>
                         </div>
                       </div>
                     </div>

                     <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Trust Score */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                            Label Trust Score
                          </h2>
                          <div className="relative z-10">
                            <p className={`text-4xl font-serif leading-none mb-2 ${result.verification.overall_trust_score < 50 ? 'text-red-600' : 'text-brand'}`}>
                              {result.verification.overall_trust_score}/100
                            </p>
                            <span className={`inline-block text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full ${result.verification.overall_trust_score < 50 ? 'bg-red-100 text-red-700' : 'bg-brand-light text-brand'}`}>
                              {result.verification.overall_trust_score < 50 ? 'Highly Deceptive' : 'Mostly Honest'}
                            </span>
                          </div>
                        </div>
                     </div>

                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       {/* Contradictions & Loopholes */}
                       <div className="space-y-6">
                         <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                           <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                             Direct Contradictions
                           </h2>
                           {result.verification.contradictions?.length > 0 ? (
                             <div className="space-y-4">
                               {result.verification.contradictions.map((c: any, i: number) => (
                                 <div key={i} className="p-4 bg-red-50 rounded-xl border border-red-100">
                                   <div className="flex justify-between items-start mb-2">
                                     <span className="font-bold text-sm text-red-800">Claim: "{c.claim}"</span>
                                     <span className="text-[9px] uppercase font-bold bg-red-200 text-red-700 px-2 py-1 rounded-full">Busted</span>
                                   </div>
                                   <p className="text-xs text-red-600 mb-2">Found: <span className="font-bold">{c.contradicting_ingredient}</span></p>
                                   <p className="text-xs text-red-700 italic">{c.explanation}</p>
                                 </div>
                               ))}
                             </div>
                           ) : (
                             <p className="text-sm text-gray-500 italic">No direct ingredient contradictions found.</p>
                           )}
                         </div>

                         <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                           <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                             Regulatory Loopholes
                           </h2>
                           {result.verification.loopholes?.length > 0 ? (
                             <div className="space-y-4">
                               {result.verification.loopholes.map((l: any, i: number) => (
                                 <div key={i} className="p-4 bg-yellow-50 rounded-xl border border-yellow-100">
                                   <div className="flex justify-between items-start mb-2">
                                     <span className="font-bold text-sm text-yellow-800">Claim: "{l.claim}"</span>
                                   </div>
                                   <p className="text-xs text-yellow-700 mb-2">{l.true_meaning}</p>
                                   <p className="text-xs text-yellow-800 bg-yellow-100 p-2 rounded-lg">{l.reality_check}</p>
                                 </div>
                               ))}
                             </div>
                           ) : (
                             <p className="text-sm text-gray-500 italic">No sneaky legal loopholes detected.</p>
                           )}
                         </div>
                       </div>

                       {/* Buzzwords */}
                       <div className="space-y-6">
                         <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                           <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                             Buzzword Decoder
                           </h2>
                           {result.verification.buzzwords?.length > 0 ? (
                             <div className="space-y-4">
                               {result.verification.buzzwords.map((b: any, i: number) => (
                                 <div key={i} className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                                   <div className="flex justify-between items-start mb-2">
                                     <span className="font-bold text-sm text-gray-800">"{b.word}"</span>
                                     <span className="text-[9px] uppercase font-bold bg-gray-200 text-gray-600 px-2 py-1 rounded-full">Fluff: {b.fluff_score}%</span>
                                   </div>
                                   <p className="text-xs text-gray-600">{b.explanation}</p>
                                 </div>
                               ))}
                             </div>
                           ) : (
                             <p className="text-sm text-gray-500 italic">No marketing fluff detected.</p>
                           )}
                         </div>
                       </div>
                     </div>
                     <div className="flex justify-center mt-8">
                       <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                         Scan Another Image
                       </button>
                     </div>
                   </div>
                 )}
"""

target = "                 {scanMode === 'nutrition' && result && ("

if "Claims Verifier" not in content and target in content:
    content = content.replace(target, claims_render + "\n" + target)
    with open('frontend/src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
        print("Patched results")
else:
    print("Already patched or target not found")

