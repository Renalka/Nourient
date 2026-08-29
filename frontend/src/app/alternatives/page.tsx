"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";

export default function AlternativesPage() {
  const { getToken } = useAuth();
  
  // Minimal manual input for demo purposes
  const [category, setCategory] = useState('Snack');
  const [sugar, setSugar] = useState(15.0);
  const [protein, setProtein] = useState(2.0);
  const [price, setPrice] = useState(100.0);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [alternatives, setAlternatives] = useState<any[]>([]);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setAlternatives([]);

    try {
      const response = await fetch('http://localhost:8006/api/v1/alternatives/find', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: category,
          current_sugar: sugar,
          current_protein: protein,
          current_price: price
        }),
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
    <main className="min-h-screen bg-white text-black font-sans selection:bg-black selection:text-white p-6 md:p-12">
      <div className="max-w-5xl mx-auto space-y-12">
        <header className="border-b border-black pb-6 relative">
          <Link href="/dashboard" className="absolute top-0 right-0 text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black hover:underline underline-offset-4">
            &larr; Dashboard
          </Link>
          <h1 className="text-3xl font-bold tracking-tighter uppercase">Better Alternatives</h1>
          <p className="mt-2 text-sm text-gray-500 uppercase tracking-widest">Discover Healthier Options</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <section className="md:col-span-1 border border-black p-6 space-y-4 h-fit">
            <h2 className="text-sm font-bold uppercase tracking-widest border-b border-gray-200 pb-2 mb-4">Current Product</h2>
            
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
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Sugar (g)</label>
              <input 
                type="number" 
                value={sugar} 
                onChange={e => setSugar(Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Protein (g)</label>
              <input 
                type="number" 
                value={protein} 
                onChange={e => setProtein(Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-widest text-gray-500 mb-1">Price (₹)</label>
              <input 
                type="number" 
                value={price} 
                onChange={e => setPrice(Number(e.target.value))}
                className="w-full border border-black p-2 text-sm"
              />
            </div>

            <button
              onClick={handleSearch}
              disabled={loading}
              className="w-full mt-4 px-4 py-3 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 disabled:opacity-50 transition-colors"
            >
              {loading ? 'Searching DB...' : 'Find Better Options'}
            </button>
            
            {error && <div className="text-xs text-red-500 font-bold uppercase mt-2">{error}</div>}
          </section>

          <section className="md:col-span-2 space-y-6">
            <h2 className="text-xl font-bold tracking-tighter uppercase mb-6">Recommendations</h2>
            
            {alternatives.length === 0 && !loading && (
              <div className="border border-dashed border-gray-300 p-12 text-center text-gray-400 uppercase tracking-widest text-sm">
                Enter current product macros to see alternatives.
              </div>
            )}

            <div className="grid gap-4">
              {alternatives.map((alt, idx) => (
                <div key={alt.product_id} className="border border-black flex flex-col md:flex-row">
                  <div className="bg-black text-white p-6 flex flex-col justify-center items-center w-full md:w-32">
                    <span className="text-3xl font-bold">{alt.overall_score}</span>
                    <span className="text-[10px] uppercase tracking-widest">Score</span>
                  </div>
                  
                  <div className="p-6 flex-grow flex flex-col justify-between">
                    <div>
                      <h3 className="text-xl font-bold tracking-tighter uppercase">{alt.name}</h3>
                      <p className="text-xs text-gray-500 uppercase tracking-widest mb-4">{alt.brand}</p>
                    </div>
                    
                    <div className="flex gap-2 flex-wrap">
                      {alt.improvements.map((imp: string, i: number) => (
                        <span key={i} className="px-2 py-1 bg-green-50 text-green-700 border border-green-200 text-xs font-bold uppercase tracking-wider">
                          {imp}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="p-6 border-t md:border-t-0 md:border-l border-gray-200 bg-gray-50 flex flex-col justify-center min-w-[120px]">
                    <span className="text-xl font-bold">₹{alt.price_inr}</span>
                    <span className="text-xs text-gray-500 uppercase tracking-widest">Price</span>
                    
                    {alt.protein_per_rupee > 0 && (
                      <div className="mt-4 border-t border-gray-300 pt-2">
                        <span className="text-sm font-bold block">{alt.protein_per_rupee}g</span>
                        <span className="text-[9px] text-gray-500 uppercase tracking-widest">Protein per ₹</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
