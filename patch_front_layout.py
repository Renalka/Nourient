import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# 1. Replace Visual Vibe widget with Explicit Claims widget
old_visual_vibe = """                        {/* Visual Vibe */}
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
                        </div>"""

new_explicit_claims = """                        {/* Explicit Claims */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            Explicit Claims
                          </h2>
                          <div className="relative z-10 flex flex-wrap gap-2">
                             {result.explicit_claims?.length > 0 ? result.explicit_claims.slice(0, 3).map((claim: string, i: number) => (
                               <span key={i} className="text-[9px] font-bold uppercase tracking-widest bg-blue-50 border border-blue-100 text-blue-700 px-2 py-1 rounded-md">{claim}</span>
                             )) : (
                               <span className="text-xs text-gray-400 font-medium italic">No claims detected</span>
                             )}
                          </div>
                        </div>"""

if "Visual Vibe" in content:
    content = content.replace(old_visual_vibe, new_explicit_claims)
else:
    print("Visual Vibe not found")

# 2. Add visual cues into Health Halo Breakdown
old_health_halo = """                       {/* Left Column: Visual Analysis */}
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
                       </div>"""

new_health_halo = """                       {/* Left Column: Visual Analysis */}
                       <div className="space-y-6">
                         {result.health_halo && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                               Health Halo Breakdown
                             </h2>
                             <div className="p-4 rounded-xl border-l-4 border-yellow-500 bg-yellow-50 mb-4">
                               <p className="text-sm text-yellow-800 leading-relaxed font-medium">{result.health_halo.reasoning}</p>
                             </div>
                             {result.health_halo.visual_cues && result.health_halo.visual_cues.length > 0 && (
                               <div className="mt-4 pt-4 border-t border-gray-100">
                                 <h3 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-3">Detected Visual Cues</h3>
                                 <div className="flex flex-wrap gap-2">
                                   {result.health_halo.visual_cues.map((cue: string, i: number) => (
                                     <span key={i} className="text-[10px] font-bold uppercase tracking-widest bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full">{cue}</span>
                                   ))}
                                 </div>
                               </div>
                             )}
                           </div>
                         )}
                       </div>"""

if "Left Column: Visual Analysis" in content:
    content = content.replace(old_health_halo, new_health_halo)
else:
    print("Left column visual analysis not found")

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

