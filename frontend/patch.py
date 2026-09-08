import re

with open('src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Remove imports we don't need
content = content.replace("import SidebarLayout from '@/components/SidebarLayout';\n", "")
content = content.replace("import AvatarMenu from '@/components/AvatarMenu';\n", "")
content = content.replace("import Breadcrumbs from '@/components/Breadcrumbs';\n", "")

# We need to replace everything from "  return (\n    <SidebarLayout" to the end of the file.
split_point = content.find("  return (\n    <SidebarLayout")

if split_point != -1:
    before = content[:split_point]
    
    after = """  return (
    <div className="min-h-screen bg-[#F9F9F7] font-sans text-foreground">
      {/* Standalone Header */}
      <header className="bg-white border-b border-gray-200 px-4 md:px-8 py-4 flex justify-between items-center sticky top-0 z-50 shadow-sm">
        <Link href="/" className="flex items-center gap-3">
          <img src="/icon.png" alt="Nourient Logo" className="w-6 h-6 object-contain" />
          <span className="font-bold tracking-widest text-[12px] text-brand uppercase hidden md:block">Nourient</span>
        </Link>
        
        {/* Step Indicators */}
        <div className="flex items-center gap-2 sm:gap-4 text-[10px] sm:text-xs font-medium">
            <div className={`flex items-center gap-1 sm:gap-2 ${step >= 1 ? 'text-foreground' : 'text-gray-400'}`}>
              <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 1 ? 'bg-brand text-white' : 'bg-gray-100'}`}>1</span>
              <span className="hidden sm:inline">Capture</span>
            </div>
            <div className="w-2 sm:w-6 h-px bg-gray-200"></div>
            <div className={`flex items-center gap-1 sm:gap-2 ${step >= 2 ? 'text-foreground' : 'text-gray-400'}`}>
              <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 2 ? 'bg-brand text-white' : 'bg-gray-100'}`}>2</span>
              <span className="hidden sm:inline">Review</span>
            </div>
            <div className="w-2 sm:w-6 h-px bg-gray-200"></div>
            <div className={`flex items-center gap-1 sm:gap-2 ${step >= 3 ? 'text-foreground' : 'text-gray-400'}`}>
              <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 3 ? 'bg-brand text-white' : 'bg-gray-100'}`}>3</span>
              <span className="hidden sm:inline">Analyze</span>
            </div>
            <div className="w-2 sm:w-6 h-px bg-gray-200"></div>
            <div className={`flex items-center gap-1 sm:gap-2 ${step >= 4 ? 'text-foreground' : 'text-gray-400'}`}>
              <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 4 ? 'bg-brand text-white' : 'bg-gray-100'}`}>4</span>
            </div>
        </div>
        
        {/* Right Nav */}
        <div>
          {user ? (
            <Link href="/dashboard" className="text-xs font-bold text-gray-500 hover:text-brand transition-colors bg-gray-50 px-4 py-2 rounded-full border border-gray-200">Dashboard</Link>
          ) : (
            <Link href="/auth" className="text-xs font-bold text-brand hover:text-brand-dark transition-colors bg-brand-light px-4 py-2 rounded-full">Log In</Link>
          )}
        </div>
      </header>

      <main className="p-4 sm:p-8 max-w-5xl mx-auto pb-32">
        <div className="w-full">
            {/* Step 1: Capture */}
            {step === 1 && (
              <div className="max-w-2xl mx-auto space-y-6">
                <div className="text-center mb-8">
                  <h1 className="text-2xl font-serif text-brand mb-2">Scan Ingredient Label</h1>
                  <p className="text-sm text-gray-500">Take a clear, well-lit photo of the ingredient list.</p>
                </div>

                {!isCameraActive ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button 
                      onClick={startCamera}
                      className="group flex flex-col items-center justify-center gap-4 p-8 border-2 border-dashed border-gray-200 rounded-3xl bg-white hover:border-brand hover:bg-brand-light transition-all h-64"
                    >
                      <div className="w-16 h-16 rounded-full bg-brand-light flex items-center justify-center group-hover:bg-brand text-brand group-hover:text-white transition-colors">
                        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                      </div>
                      <span className="font-bold text-gray-700">Open Camera</span>
                    </button>

                    <div 
                      className="group flex flex-col items-center justify-center gap-4 p-8 border-2 border-dashed border-gray-200 rounded-3xl bg-white hover:border-brand hover:bg-brand-light transition-all h-64 cursor-pointer"
                      onClick={() => uploadInputRef.current?.click()}
                    >
                      <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center group-hover:bg-brand text-gray-500 group-hover:text-white transition-colors">
                        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                      </div>
                      <span className="font-bold text-gray-700">Upload Photo</span>
                      <input 
                        type="file" 
                        accept="image/*"
                        className="hidden" 
                        ref={uploadInputRef}
                        onChange={handleFileUpload}
                      />
                    </div>
                  </div>
                ) : (
                  <div className="relative rounded-3xl overflow-hidden bg-black aspect-[3/4] sm:aspect-[4/3] shadow-xl">
                    <video ref={videoRef} autoPlay playsInline className="absolute inset-0 w-full h-full object-cover" />
                    
                    {/* Viewfinder overlay */}
                    <div className="absolute inset-0 border-[40px] border-black/40 pointer-events-none">
                      <div className="w-full h-full border-2 border-dashed border-white/50 rounded-lg"></div>
                    </div>

                    <div className="absolute bottom-6 left-0 right-0 flex justify-center items-center gap-8">
                      <button onClick={stopCamera} className="p-4 rounded-full bg-white/20 text-white backdrop-blur-md hover:bg-white/30 transition-colors">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                      </button>
                      <button onClick={capturePhoto} className="w-16 h-16 rounded-full bg-white border-4 border-gray-300 hover:border-brand transition-colors shadow-lg"></button>
                    </div>
                    <canvas ref={canvasRef} className="hidden" />
                  </div>
                )}
              </div>
            )}

            {/* Step 2: Review */}
            {step === 2 && previewUrl && (
              <div className="max-w-2xl mx-auto space-y-6">
                <div className="text-center mb-6">
                  <h1 className="text-2xl font-serif text-brand mb-2">Review Photo</h1>
                  <p className="text-sm text-gray-500">Ensure the text is legible before analyzing.</p>
                </div>
                
                <div className="rounded-3xl overflow-hidden bg-white border border-gray-200 shadow-sm p-2 relative h-[500px]">
                  <img src={previewUrl} alt="Preview" className="w-full h-full object-contain rounded-2xl" />
                </div>

                {error && (
                  <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm border border-red-100 flex items-center gap-2">
                    <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    {error}
                  </div>
                )}

                <div className="flex gap-4">
                  <button onClick={handleRetake} className="flex-1 py-4 bg-white border border-gray-200 rounded-xl font-bold text-gray-600 hover:bg-gray-50 transition-colors">Retake</button>
                  <button onClick={handleAnalyze} className="flex-1 py-4 bg-brand text-white rounded-xl font-bold hover:bg-brand-dark transition-colors shadow-md">Analyze</button>
                </div>
              </div>
            )}

            {/* Step 3: Loading */}
            {step === 3 && (
              <div className="max-w-2xl mx-auto space-y-8 py-20 text-center">
                 <div className="relative w-32 h-32 mx-auto">
                   <div className="absolute inset-0 rounded-full border-4 border-brand-light"></div>
                   <div className="absolute inset-0 rounded-full border-4 border-brand border-t-transparent animate-spin"></div>
                   <div className="absolute inset-0 flex items-center justify-center">
                     <svg className="w-10 h-10 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                   </div>
                 </div>
                 
                 <div className="space-y-3">
                   <h2 className="text-xl font-serif text-brand">Running Deep Scan</h2>
                   <p className="text-sm text-gray-500 font-mono tracking-widest uppercase">{progressText}</p>
                 </div>

                 <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                   <div className="bg-brand h-1.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
                 </div>
              </div>
            )}

            {/* Step 4: Results */}
            {step === 4 && result && (
              <div className="space-y-6">
                 
                 {/* Top Hero Banner */}
                 <div className="relative w-full h-[250px] md:h-[300px] rounded-3xl overflow-hidden shadow-lg border border-gray-200">
                    <img src="/fresh_food.jpg" alt="Fresh Food Background" className="absolute inset-0 w-full h-full object-cover z-0" />
                    {/* Dark gradient overlay to ensure text readability */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/10 z-10"></div>
                    
                    <div className="absolute inset-0 z-20 flex flex-col justify-end p-6 md:p-10">
                       <h1 className="text-3xl md:text-5xl font-serif text-white mb-2 leading-tight">
                         {result.extracted_data?.name || "Unnamed Product"}
                       </h1>
                       <div className="flex items-center gap-4">
                         <p className="text-sm md:text-base text-gray-200 uppercase tracking-widest font-medium">
                           {result.extracted_data?.brand || "Unknown Brand"}
                         </p>
                       </div>
                       
                       {/* Add to Basket Action */}
                       <div className="absolute top-6 right-6 md:top-10 md:right-10 flex flex-col items-end">
                         <button 
                           onClick={handleAddToBasket} 
                           disabled={addingToBasket}
                           className="px-6 py-2 bg-white text-brand rounded-xl text-sm font-bold hover:bg-gray-50 hover:scale-105 active:scale-95 disabled:opacity-50 transition-all shadow-md"
                         >
                           {addingToBasket ? 'Adding...' : 'Add to Basket'}
                         </button>
                         {basketMsg && <span className="text-[10px] text-white mt-2 font-bold uppercase tracking-widest bg-black/60 backdrop-blur-sm px-3 py-1 rounded-full">{basketMsg}</span>}
                       </div>
                    </div>
                 </div>

                 {/* Scientific Grade Widget */}
                 {result.score && (
                   <div className={`p-8 rounded-3xl border flex flex-col md:flex-row items-center gap-8 ${getGrade(result.score.composite_score).bg} ${getGrade(result.score.composite_score).color.replace('text-', 'border-')}/20 shadow-sm`}>
                     <div className="relative flex-shrink-0 w-32 h-32">
                       <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                         <path className="text-gray-200/50" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
                         <path className={getGrade(result.score.composite_score).color} strokeDasharray={`${result.score.composite_score}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
                       </svg>
                       <div className="absolute inset-0 flex flex-col items-center justify-center">
                         <span className="text-4xl font-bold font-serif">{Math.round(result.score.composite_score)}</span>
                       </div>
                     </div>
                     
                     <div className="flex-1 flex flex-col sm:flex-row gap-6 sm:gap-10">
                       <div>
                         <p className="text-xs font-bold uppercase tracking-widest mb-1 opacity-70">Scientific Verdict</p>
                         <p className="text-2xl font-bold">{getGrade(result.score.composite_score).label}</p>
                       </div>
                       <div>
                         <p className={`text-xs font-bold uppercase tracking-widest mb-1 ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-700' : 'text-brand'}`}>Nourient's Recommendation</p>
                         <p className={`text-lg font-serif leading-none ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-900' : 'text-brand-dark'}`}>{result.score.overall_recommendation}</p>
                       </div>
                     </div>
                   </div>
                 )}

                 <div className="grid grid-cols-1 gap-6">

                    {/* TrueLabel Auditor */}
                    {result.extracted_data?.audit && (
                      <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                        <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-6">TrueLabel Auditor</h2>
                        <div className="space-y-4">
                          {result.extracted_data.audit.map((audit: any, idx: number) => (
                            <div key={idx} className={`p-4 rounded-xl border-l-4 ${audit.verdict === 'Deceptive' ? 'border-red-500 bg-red-50' : 'border-green-500 bg-brand-light'}`}>
                              <div className="flex justify-between items-start mb-2">
                                <span className="font-bold text-sm text-foreground">"{audit.claim}"</span>
                                <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded-full ${audit.verdict === 'Deceptive' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-brand'}`}>
                                  {audit.verdict}
                                </span>
                              </div>
                              <p className="text-xs text-gray-600">{audit.reasoning}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                 </div>

                 {/* Ingredient Detective */}
                 {result.detective && (
                   <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                     <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex justify-between items-center">
                       Ingredient Detective
                       {(result.detective.flagged_ingredients?.length > 0 || result.detective.decoded_additives?.length > 0) && (
                         <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Active</span>
                       )}
                     </h2>
                     <p className="text-sm text-gray-600 mb-6 leading-relaxed border-b border-gray-100 pb-6">
                       <span className="font-bold block mb-2 text-xs text-gray-400 uppercase tracking-widest">Raw Ingredient List</span>
                       {result.extracted_data?.ingredients?.map((ing: any) => 
                         ing.percentage ? `${ing.name} (${ing.percentage}%)` : ing.name
                       ).join(', ') || 'No ingredients detected.'}
                     </p>

                     {/* Deterministic Unified Decoder */}
                     {result.detective.decoded_additives?.length > 0 && (
                       <div className="mb-8">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Ingredients Decoded</h3>
                         <div className="space-y-2">
                           {result.detective.decoded_additives.map((additive: any, i: number) => (
                             <div key={i} className="flex flex-col md:flex-row md:items-center justify-between p-3 bg-white rounded-xl border border-gray-100 shadow-sm gap-4">
                               <div className="flex-1 min-w-0">
                                 <div className="flex items-center gap-2">
                                   <span className="font-bold text-sm text-foreground truncate">{additive.name}</span>
                                   {additive.code && <span className="text-[10px] text-gray-500 font-mono bg-gray-50 border border-gray-200 px-1.5 py-0.5 rounded shrink-0">{additive.code}</span>}
                                 </div>
                               </div>
                               <div className="flex flex-col sm:flex-row items-center gap-2 shrink-0">
                                 <span className="w-full sm:w-[130px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.source}</span>
                                 <span className="w-full sm:w-[150px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.category}</span>
                                 <span className={`w-full sm:w-[100px] text-[9px] uppercase font-bold tracking-widest px-2 py-1 rounded-full text-center shrink-0 ${
                                   additive.risk_level.toLowerCase() === 'safe' ? 'bg-green-100 text-green-700 border border-green-200' :
                                   additive.risk_level.toLowerCase() === 'moderate risk' || additive.risk_level.toLowerCase() === 'permitted additive' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                                   additive.risk_level.toLowerCase() === 'unknown' ? 'bg-gray-100 text-gray-600 border border-gray-200' :
                                   'bg-red-100 text-red-700 border border-red-200'
                                 }`}>
                                   {additive.risk_level}
                                 </span>
                               </div>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* AI Flagger */}
                     {result.detective.flagged_ingredients?.length > 0 && (
                       <div>
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Flagged Concerns</h3>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           {result.detective.flagged_ingredients.map((ing: any, i: number) => (
                             <div key={i} className="p-4 bg-red-50 rounded-xl border border-red-100">
                               <div className="flex justify-between items-center mb-2">
                                 <span className="font-bold text-sm text-red-700">{ing.name}</span>
                                 <span className="text-[10px] uppercase font-bold text-red-700 tracking-widest bg-red-100 px-2 py-1 rounded-full">{ing.purpose}</span>
                               </div>
                               <p className="text-xs text-red-600 mb-1">{ing.warning || ing.explanation}</p>
                               {ing.studies && <p className="text-[10px] text-red-400 italic mt-2 border-t border-red-100 pt-2">Studies: {ing.studies}</p>}
                             </div>
                           ))}
                         </div>
                       </div>
                     )}
                   </div>
                 )}
                 
                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-bold text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
              </div>
            )}

        </div>
      </main>
    </div>
  );
}
"""
    with open('src/app/scanner/page.tsx', 'w') as f:
        f.write(before + after)
else:
    print("Could not find the SidebarLayout wrapper.")

