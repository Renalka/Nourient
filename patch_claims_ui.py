import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

claims_ui = """                 {scanMode === 'claims' && result && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Claims verification header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           <h1 className="text-3xl font-serif mb-1 drop-shadow-md">Claims Verifier</h1>
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Contradictions • Loopholes • Buzzwords</p>
                         </div>
                       </div>
                     </div>

                     {/* Contradictions */}
                     {result.verification?.contradictions?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-red-100 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-red-500 mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                           Direct Contradictions
                         </h2>
                         <div className="space-y-4">
                           {result.verification.contradictions.map((c: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-red-200 bg-red-50">
                               <p className="text-lg font-bold text-red-900 mb-1">"{c.claim}"</p>
                               <p className="text-sm text-red-700 font-medium mb-3">But contains: <span className="font-black">{c.contradicting_ingredient}</span></p>
                               <p className="text-xs text-red-600 bg-white px-3 py-2 rounded-lg border border-red-100">{c.explanation}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* Loopholes */}
                     {result.verification?.loopholes?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-yellow-100 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-yellow-600 mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                           Regulatory Loopholes
                         </h2>
                         <div className="space-y-4">
                           {result.verification.loopholes.map((l: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-yellow-200 bg-yellow-50">
                               <p className="text-lg font-bold text-yellow-900 mb-1">"{l.claim}"</p>
                               <p className="text-sm text-yellow-800 font-medium mb-3">Means: <span className="font-black">{l.true_meaning}</span></p>
                               <p className="text-xs text-yellow-700 bg-white px-3 py-2 rounded-lg border border-yellow-100">{l.reality_check}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* Buzzwords */}
                     {result.verification?.buzzwords?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-brand/20 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-brand mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" /></svg>
                           Marketing Fluff
                         </h2>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           {result.verification.buzzwords.map((b: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-brand/10 bg-brand-light/30">
                               <div className="flex justify-between items-center mb-2">
                                 <p className="text-md font-bold text-brand-dark">"{b.word}"</p>
                                 <span className="text-[10px] font-bold uppercase tracking-widest bg-brand text-white px-2 py-0.5 rounded-full">Fluff: {b.fluff_score}%</span>
                               </div>
                               <p className="text-xs text-gray-700 leading-relaxed">{b.explanation}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* All Clear state */}
                     {result.verification?.contradictions?.length === 0 && result.verification?.loopholes?.length === 0 && result.verification?.buzzwords?.length === 0 && (
                       <div className="bg-white p-8 rounded-3xl border border-green-100 shadow-sm text-center">
                         <div className="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                           <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                         </div>
                         <h2 className="text-xl font-bold text-green-800 mb-2">Clean Marketing</h2>
                         <p className="text-sm text-gray-600">No major contradictions, loopholes, or fluff detected between the front claims and the ingredients list.</p>
                       </div>
                     )}

                   </div>
                 )}

                 {scanMode === 'front' && ("""

content = content.replace("                 {scanMode === 'front' && (", claims_ui)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
