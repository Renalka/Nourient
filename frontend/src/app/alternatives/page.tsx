"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import SidebarLayout from '@/components/SidebarLayout';
import { apiUrl } from '@/lib/api';

export default function AlternativesPage() {
  const { getToken } = useAuth();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const [category, setCategory] = useState('Snack');
  const [sugar, setSugar] = useState<number | ''>(15.0);
  const [protein, setProtein] = useState<number | ''>(2.0);
  const [fat, setFat] = useState<number | ''>('');
  const [satFat, setSatFat] = useState<number | ''>('');
  const [fiber, setFiber] = useState<number | ''>('');
  const [sodium, setSodium] = useState<number | ''>('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [alternatives, setAlternatives] = useState<any[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [lastQuery, setLastQuery] = useState<any>({});
  const [addingToBasket, setAddingToBasket] = useState<Record<string, boolean>>({});
  const [toast, setToast] = useState<{message: string, type: 'success' | 'error'} | null>(null);

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setAlternatives([]);
    setHasSearched(true);
    
    const queryPayload = {
      category: category,
      current_sugar: sugar === '' ? null : sugar,
      current_protein: protein === '' ? null : protein,
      current_fat: fat === '' ? null : fat,
      current_saturated_fat: satFat === '' ? null : satFat,
      current_fiber: fiber === '' ? null : fiber,
      current_sodium: sodium === '' ? null : sodium
    };
    
    setLastQuery(queryPayload);

    try {
      const response = await fetch(apiUrl('/api/v1/alternatives/find', 8006), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(queryPayload),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch alternatives");
      }

      const data = await response.json();
      setAlternatives(data.alternatives);
    } catch (err: any) {
      setError(err.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToBasket = async (alt: any) => {
    setAddingToBasket(prev => ({ ...prev, [alt.product_id]: true }));
    try {
      const token = await getToken();
      
      // 1. Evaluate Alternative using the Orchestrator Pipeline
      const evalPayload = {
        name: alt.name,
        ingredients_text: alt.ingredients_text,
        nutrition: {
          calories: { amount: alt.energy_kcal_100g || 0 },
          sugar: { amount: alt.sugar_g || 0 },
          sodium: { amount: (alt.sodium_g || 0) * 1000 }, // mg
          saturated_fat: { amount: alt.sat_fat_g || 0 },
          protein: { amount: alt.protein_g || 0 },
          fiber: { amount: alt.fiber_g || 0 }
        }
      };
      
      const evalRes = await fetch(apiUrl('/api/v1/orchestrate/evaluate-alternative'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify(evalPayload),
      });
      
      if (!evalRes.ok) throw new Error("Evaluation failed");
      const evalData = await evalRes.json();
      
      // 2. Add to Basket
      const basketPayload = {
         product_data: {
             ...evalData.extracted_data,
             score: evalData.score,
             source: "off_alternative" // Identifies it as a discovered alternative
         }
      };
      
      const basketRes = await fetch(apiUrl('/api/v1/basket/add', 8007), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify(basketPayload),
      });
      
      if (!basketRes.ok) throw new Error("Basket add failed");
      
      showToast("Added to Basket!", "success");
      
    } catch (err: any) {
      console.error(err);
      showToast("Failed to add to basket", "error");
    } finally {
      setAddingToBasket(prev => ({ ...prev, [alt.product_id]: false }));
    }
  };

  const getGradeColor = (grade: string) => {
    switch(grade?.toLowerCase()) {
      case 'a': return 'bg-green-100 text-green-800 border-green-200';
      case 'b': return 'bg-lime-100 text-lime-800 border-lime-200';
      case 'c': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'd': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'e': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <SidebarLayout
      pageTitle="Better Alternatives"
      pageSubtitle="Discover Healthier Options"
    >
      {toast && (
        <div className="fixed top-24 left-1/2 transform -translate-x-1/2 z-50 animate-fade-in flex items-center justify-center">
          <div className={`px-6 py-3 rounded-full shadow-2xl text-sm font-bold tracking-wide uppercase flex items-center gap-3 ${
            toast.type === 'success' ? 'bg-black text-white' : 'bg-red-600 text-white'
          }`}>
            {toast.type === 'success' ? (
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            ) : (
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            )}
            {toast.message}
          </div>
        </div>
      )}
      
      <div className={`transition-all duration-700 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
          
          {/* LEFT COLUMN: Filter Form */}
          <section className="lg:col-span-4">
            <div className="bg-white rounded-3xl p-8 border border-gray-100 shadow-[0_8px_30px_rgba(0,0,0,0.03)] sticky top-24">
              <div className="mb-8 relative">
                <div className="absolute -left-8 top-1 w-1 h-12 bg-brand rounded-r-lg" />
                <p className="text-[10px] font-bold tracking-[0.25em] text-brand uppercase mb-2">Search Criteria</p>
                <h2 className="text-2xl font-serif text-gray-900">Health Filters</h2>
                <p className="text-sm text-gray-500 mt-2 leading-relaxed">Set strict macro limits for your diet. The engine will instantly reject any product that breaks your rules.</p>
              </div>

              <div className="space-y-5">
                <div>
                  <label className="block text-[10px] font-bold tracking-[0.2em] text-gray-400 mb-2 uppercase">Category</label>
                  <div className="relative group">
                    <select 
                      value={category} 
                      onChange={e => setCategory(e.target.value)}
                      className="w-full appearance-none bg-gray-50 border border-gray-200 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all cursor-pointer"
                    >
                      <option value="Snack">Snack</option>
                      <option value="Cereal">Cereal</option>
                      <option value="Beverage">Beverage</option>
                      <option value="Dairy">Dairy</option>
                      <option value="Dessert">Dessert</option>
                      <option value="Biscuits & Cakes">Biscuits & Cakes</option>
                      <option value="Sauce">Sauce</option>
                      <option value="Spread">Spread</option>
                      <option value="Bread">Bread</option>
                      <option value="Chocolate">Chocolate</option>
                      <option value="Meal">Meal</option>
                      <option value="Canned Food">Canned Food</option>
                    </select>
                    <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none group-hover:text-brand transition-colors">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Max Sugar</label>
                    <input 
                      type="number" 
                      value={sugar} 
                      onChange={e => setSugar(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="g / 100g"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Min Protein</label>
                    <input 
                      type="number" 
                      value={protein} 
                      onChange={e => setProtein(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="g / 100g"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Max Fat</label>
                    <input 
                      type="number" 
                      value={fat} 
                      onChange={e => setFat(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="Optional"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Max Sat Fat</label>
                    <input 
                      type="number" 
                      value={satFat} 
                      onChange={e => setSatFat(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="Optional"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Min Fiber</label>
                    <input 
                      type="number" 
                      value={fiber} 
                      onChange={e => setFiber(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="Optional"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold tracking-[0.15em] text-gray-400 mb-2 uppercase truncate">Max Sodium</label>
                    <input 
                      type="number" 
                      step="0.01"
                      value={sodium} 
                      onChange={e => setSodium(e.target.value === '' ? '' : Number(e.target.value))}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand/20 focus:border-brand transition-all placeholder:text-gray-300 placeholder:font-normal"
                      placeholder="Optional"
                    />
                  </div>
                </div>

                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="w-full mt-6 flex items-center justify-center gap-3 px-6 py-4 bg-[#0D0D0D] text-white rounded-xl text-sm font-bold uppercase tracking-widest hover:bg-black disabled:opacity-50 transition-all hover:scale-[1.02] active:scale-[0.98] shadow-lg"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                      Searching Database
                    </span>
                  ) : (
                    <>
                      <span>Find Better Options</span>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </>
                  )}
                </button>
                
                {error && (
                  <div className="flex items-center gap-2 text-xs text-red-600 bg-red-50 p-3 rounded-lg font-medium">
                    <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                    {error}
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* RIGHT COLUMN: Results */}
          <section className="lg:col-span-8">
            {alternatives.length === 0 && !loading && !hasSearched && (
              <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-center px-6">
                <div className="w-24 h-24 mb-6 rounded-full bg-brand/5 flex items-center justify-center">
                  <svg className="w-10 h-10 text-brand/40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                </div>
                <h3 className="text-xl font-serif text-gray-900 mb-2">Ready to explore?</h3>
                <p className="text-sm text-gray-500 max-w-sm">Enter your nutritional thresholds on the left to discover foods that meet your strict health goals.</p>
              </div>
            )}

            {alternatives.length === 0 && !loading && hasSearched && (
              <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-center px-6 bg-white rounded-3xl border border-gray-100 shadow-sm animate-card-enter">
                <div className="w-20 h-20 mb-6 rounded-2xl bg-orange-50 border border-orange-100 flex items-center justify-center relative">
                  <div className="absolute inset-0 bg-orange-100 rounded-2xl animate-ping opacity-20" style={{ animationDuration: '3s' }} />
                  <svg className="w-8 h-8 text-orange-400 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" /></svg>
                </div>
                <h3 className="text-xl font-serif text-gray-900 mb-2">No Match Found</h3>
                <p className="text-sm text-gray-500 max-w-md">We are forever expanding the database, but right now no products match these exact filters. Try relaxing your constraints or check back soon!</p>
              </div>
            )}

            {alternatives.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-bold text-gray-900">Recommended Products</h3>
                  <span className="text-xs font-bold bg-gray-100 text-gray-500 px-3 py-1 rounded-full">{alternatives.length} Results</span>
                </div>
                
                {alternatives.map((alt, idx) => (
                  <div 
                    key={alt.product_id} 
                    className="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] hover:border-brand/30 transition-all duration-300 overflow-hidden flex flex-col md:flex-row animate-card-enter"
                    style={{ animationDelay: `${idx * 75}ms` }}
                  >
                    <div className="md:w-32 bg-gray-50 p-6 flex flex-col justify-center items-center shrink-0 border-b md:border-b-0 md:border-r border-gray-100 relative group-hover:bg-brand/5 transition-colors">
                      <div className="relative w-16 h-16 flex items-center justify-center mb-3">
                        <svg className="w-full h-full transform -rotate-90 absolute inset-0" viewBox="0 0 36 36">
                          <path className="text-gray-200" strokeWidth="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                          <path className="text-brand transition-all duration-1000 ease-out" strokeDasharray={`${alt.betterment_score}, 100`} strokeWidth="3" stroke="currentColor" fill="none" strokeLinecap="round" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <span className="text-xl font-bold text-gray-900 relative z-10 leading-none">{alt.betterment_score}</span>
                      </div>
                      <span className="text-[9px] font-bold uppercase tracking-[0.2em] text-gray-400 text-center leading-tight">Match<br/>Score</span>
                    </div>
                    
                    <div className="p-6 flex-grow flex flex-col justify-between relative">
                      <div className="absolute right-6 top-6">
                        <span className={`text-xs font-bold px-2.5 py-1 rounded-md uppercase tracking-wider border ${getGradeColor(alt.nutriscore_grade)}`}>
                          Nutri-Score {alt.nutriscore_grade}
                        </span>
                      </div>
                      
                      <div className="pr-24 mb-4">
                        <h3 className="text-lg font-bold text-gray-900 tracking-tight leading-tight group-hover:text-brand transition-colors">{alt.name}</h3>
                        <p className="text-xs text-gray-500 font-medium tracking-wide uppercase mt-1">{alt.brand || 'Unknown Brand'}</p>
                      </div>
                      
                      <div className="flex gap-2 flex-wrap mb-5">
                        {alt.improvements.map((imp: string, i: number) => (
                          <span key={i} className="px-2.5 py-1 bg-brand/5 text-brand border border-brand/10 rounded text-[10px] font-bold uppercase tracking-wider shadow-sm">
                            {imp}
                          </span>
                        ))}
                      </div>
                      
                      <div className="text-[10px] text-gray-500 uppercase tracking-widest font-bold flex flex-wrap gap-x-5 gap-y-2 mt-auto border-t border-gray-50 pt-4 items-center justify-between">
                        <div className="flex flex-wrap gap-x-5 gap-y-2">
                          {lastQuery.current_sugar !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Sug: <span className="text-gray-900">{alt.sugar_g != null ? alt.sugar_g + 'g' : '--'}</span></span>}
                          {lastQuery.current_protein !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Pro: <span className="text-gray-900">{alt.protein_g != null ? alt.protein_g + 'g' : '--'}</span></span>}
                          {lastQuery.current_fat !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Fat: <span className="text-gray-900">{alt.fat_g != null ? alt.fat_g + 'g' : '--'}</span></span>}
                          {lastQuery.current_saturated_fat !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Sat Fat: <span className="text-gray-900">{alt.sat_fat_g != null ? alt.sat_fat_g + 'g' : '--'}</span></span>}
                          {lastQuery.current_fiber !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Fiber: <span className="text-gray-900">{alt.fiber_g != null ? alt.fiber_g + 'g' : '--'}</span></span>}
                          {lastQuery.current_sodium !== null && <span className="flex items-center gap-1.5"><span className="w-1 h-1 rounded-full bg-gray-300"></span> Sod: <span className="text-gray-900">{alt.sodium_g != null ? alt.sodium_g + 'g' : '--'}</span></span>}
                        </div>
                        
                        <button 
                          onClick={() => handleAddToBasket(alt)}
                          disabled={addingToBasket[alt.product_id]}
                          className="shrink-0 flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:hover:scale-100 shadow-sm"
                        >
                          {addingToBasket[alt.product_id] ? (
                            <svg className="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                          ) : (
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                          )}
                          <span>Basket</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

        </div>
      </div>
    </SidebarLayout>
  );
}
