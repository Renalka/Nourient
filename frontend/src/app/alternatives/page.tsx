"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import SidebarLayout from '@/components/SidebarLayout';

export default function AlternativesPage() {
  const { getToken } = useAuth();
  
  // Minimal manual input for demo purposes
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
      const response = await fetch('http://localhost:8006/api/v1/alternatives/find', {
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

  return (
    <SidebarLayout
      pageTitle="Better Alternatives"
      pageSubtitle="Discover Healthier Options"
    >
      <div className="space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <section className="md:col-span-1 border border-black p-6 space-y-4 h-fit">
            <h2 className="text-lg font-serif border-b border-gray-200 pb-2 mb-4">Current Product</h2>
            
            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Category</label>
              <select 
                value={category} 
                onChange={e => setCategory(e.target.value)}
                className="w-full border border-black p-2 text-sm font-bold uppercase"
              >
                <option value="Snack">Snack</option>
                <option value="Cereal">Cereal</option>
                <option value="Beverage">Beverage</option>
              </select>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Sugar (per 100g/ml)</label>
              <input 
                type="number" 
                value={sugar} 
                onChange={e => setSugar(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Protein (per 100g/ml)</label>
              <input 
                type="number" 
                value={protein} 
                onChange={e => setProtein(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Fat (per 100g/ml)</label>
              <input 
                type="number" 
                value={fat} 
                onChange={e => setFat(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Saturated Fat (per 100g/ml)</label>
              <input 
                type="number" 
                value={satFat} 
                onChange={e => setSatFat(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Fiber (per 100g/ml)</label>
              <input 
                type="number" 
                value={fiber} 
                onChange={e => setFiber(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Sodium (per 100g/ml)</label>
              <input 
                type="number" 
                step="0.01"
                value={sodium} 
                onChange={e => setSodium(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
                placeholder="Optional"
              />
            </div>

            <button
              onClick={handleSearch}
              disabled={loading}
              className="w-full mt-4 px-4 py-3 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 disabled:opacity-50 transition-colors"
            >
              {loading ? 'Searching...' : 'Find Better Options'}
            </button>
            
            {error && <div className="text-xs text-red-500 font-bold uppercase mt-2">{error}</div>}
          </section>

          <section className="md:col-span-2 space-y-6">
            <h2 className="text-xl font-bold tracking-tighter uppercase mb-6">Recommendations</h2>
            
            {alternatives.length === 0 && !loading && !hasSearched && (
              <div className="border border-dashed border-gray-300 p-12 text-center text-gray-400 uppercase tracking-widest text-sm">
                Enter current product macros to see alternatives.
              </div>
            )}

            {alternatives.length === 0 && !loading && hasSearched && (
              <div className="border border-dashed border-gray-300 p-12 text-center text-gray-400 text-sm">
                <span className="uppercase tracking-widest font-bold block mb-2 text-gray-500">No Match Found</span>
                We are forever expanding the database, but right now we don't have any recommendation that beats these macros. Check back soon!
              </div>
            )}

            <div className="grid gap-4">
              {alternatives.map((alt, idx) => (
                <div key={alt.product_id} className="border border-black flex flex-col md:flex-row">
                  <div className="bg-black text-white p-6 flex flex-col justify-center items-center w-full md:w-32 shrink-0">
                    <span className="text-3xl font-bold">{alt.betterment_score}</span>
                    <span className="text-[10px] uppercase tracking-widest text-center mt-1">Match<br/>Score</span>
                  </div>
                  
                  <div className="p-6 flex-grow flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start gap-4">
                        <h3 className="text-xl font-bold tracking-tighter uppercase">{alt.name}</h3>
                        <span className="text-xs font-bold px-2 py-1 bg-gray-200 text-black uppercase tracking-wider shrink-0">
                          Nutri-Score {alt.nutriscore_grade}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 uppercase tracking-widest mb-4">{alt.brand}</p>
                    </div>
                    
                    <div className="flex gap-2 flex-wrap mb-3">
                      {alt.improvements.map((imp: string, i: number) => (
                        <span key={i} className="px-2 py-1 bg-green-50 text-green-700 border border-green-200 text-xs font-bold uppercase tracking-wider">
                          {imp}
                        </span>
                      ))}
                    </div>
                    <div className="text-xs text-gray-400 uppercase tracking-widest font-bold flex flex-wrap gap-x-4 gap-y-1 mt-2 border-t border-gray-100 pt-3">
                      {lastQuery.current_sugar !== null && <span>Sug: {alt.sugar_g != null ? alt.sugar_g + 'g' : '--'}</span>}
                      {lastQuery.current_protein !== null && <span>Pro: {alt.protein_g != null ? alt.protein_g + 'g' : '--'}</span>}
                      {lastQuery.current_fat !== null && <span>Fat: {alt.fat_g != null ? alt.fat_g + 'g' : '--'}</span>}
                      {lastQuery.current_saturated_fat !== null && <span>Sat Fat: {alt.sat_fat_g != null ? alt.sat_fat_g + 'g' : '--'}</span>}
                      {lastQuery.current_fiber !== null && <span>Fiber: {alt.fiber_g != null ? alt.fiber_g + 'g' : '--'}</span>}
                      {lastQuery.current_sodium !== null && <span>Sodium: {alt.sodium_g != null ? alt.sodium_g + 'g' : '--'}</span>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </SidebarLayout>
  );
}
