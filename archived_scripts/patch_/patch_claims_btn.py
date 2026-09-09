import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

nutr_btn = """                      <button 
                        onClick={() => setScanMode('nutrition')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'nutrition' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'nutrition' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'nutrition' ? 'text-brand-dark' : 'text-gray-700'}`}>Nutrition Facts</h3>
                            <p className="text-xs text-gray-500">Expose portion loopholes & empty calories</p>
                          </div>
                        </div>
                      </button>"""

claims_btn = """
                      <button 
                        onClick={() => setScanMode('claims')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'claims' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'claims' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'claims' ? 'text-brand-dark' : 'text-gray-700'}`}>Claims Verifier</h3>
                            <p className="text-xs text-gray-500">Cross-reference marketing with ingredients</p>
                          </div>
                        </div>
                      </button>"""

if "Claims Verifier" not in content:
    content = content.replace(nutr_btn, nutr_btn + claims_btn)
    with open('frontend/src/app/scanner/page.tsx', 'w') as f:
        f.write(content)
    print("Added Claims Verifier button")
else:
    print("Button already there")
