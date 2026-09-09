import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

detailed_audit_code = """                     {/* Detailed Claims Audit */}
                     <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm mt-8">
                       <h2 className="text-xl font-serif text-gray-900 mb-6 flex items-center gap-2">
                         <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
                         Detailed Claims Audit
                       </h2>
                       <div className="space-y-4">
                         {result.explicit_claims?.length > 0 ? result.explicit_claims.map((claim: string, i: number) => {
                           const contradiction = result.verification?.contradictions?.find((c: any) => c.claim === claim);
                           const loophole = result.verification?.loopholes?.find((l: any) => l.claim === claim);
                           const buzzword = result.verification?.buzzwords?.find((b: any) => b.word === claim);

                           let status = 'CLEAN';
                           if (contradiction) status = 'CONTRADICTION';
                           else if (loophole) status = 'LOOPHOLE';
                           else if (buzzword) status = 'BUZZWORD';

                           return (
                             <div key={i} className={`p-5 rounded-2xl border ${status === 'CLEAN' ? 'border-green-100 bg-green-50' : status === 'CONTRADICTION' ? 'border-red-100 bg-red-50' : status === 'LOOPHOLE' ? 'border-yellow-100 bg-yellow-50' : 'border-brand/20 bg-brand-light/30'}`}>
                               <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                                 <p className="text-lg font-bold text-gray-900">&quot;{claim}&quot;</p>
                                 <div>
                                   {status === 'CLEAN' && <span className="text-[10px] font-bold uppercase tracking-widest bg-green-200 text-green-800 px-3 py-1 rounded-full">No Flags Detected</span>}
                                   {status === 'CONTRADICTION' && <span className="text-[10px] font-bold uppercase tracking-widest bg-red-200 text-red-800 px-3 py-1 rounded-full">Direct Contradiction</span>}
                                   {status === 'LOOPHOLE' && <span className="text-[10px] font-bold uppercase tracking-widest bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full">Regulatory Loophole</span>}
                                   {status === 'BUZZWORD' && <span className="text-[10px] font-bold uppercase tracking-widest bg-brand text-white px-3 py-1 rounded-full">Marketing Fluff</span>}
                                 </div>
                               </div>
                               
                               <div className="text-sm">
                                 {status === 'CLEAN' && <p className="text-green-700">This claim appears to be standard and does not trigger our deception database.</p>}
                                 
                                 {status === 'CONTRADICTION' && (
                                   <>
                                     <p className="text-red-700 font-medium mb-2">But contains: <span className="font-black">{contradiction.contradicting_ingredient}</span></p>
                                     <p className="text-red-600 bg-white px-4 py-3 rounded-xl border border-red-100 leading-relaxed">{contradiction.explanation}</p>
                                   </>
                                 )}
                                 
                                 {status === 'LOOPHOLE' && (
                                   <>
                                     <p className="text-yellow-800 font-medium mb-2">Means: <span className="font-black">{loophole.true_meaning}</span></p>
                                     <p className="text-yellow-700 bg-white px-4 py-3 rounded-xl border border-yellow-100 leading-relaxed">{loophole.reality_check}</p>
                                   </>
                                 )}
                                 
                                 {status === 'BUZZWORD' && (
                                   <p className="text-gray-700 bg-white px-4 py-3 rounded-xl border border-brand/10 leading-relaxed">{buzzword.explanation}</p>
                                 )}
                               </div>
                             </div>
                           );
                         }) : (
                           <div className="bg-gray-50 border border-gray-100 rounded-2xl p-6 text-center">
                             <p className="text-gray-500 font-medium">No explicit marketing claims detected on the front of the packaging.</p>
                           </div>
                         )}
                       </div>
                     </div>

                   </div>
                 )}"""

# Replace the closing `</div>` and `)}` for scanMode === 'claims'
old_ending = """                   </div>
                 )}"""

content = content.replace(old_ending, detailed_audit_code)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
