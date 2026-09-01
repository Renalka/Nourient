'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import SidebarLayout from '@/components/SidebarLayout';
import AvatarMenu from '@/components/AvatarMenu';
import Breadcrumbs from '@/components/Breadcrumbs';

export default function DictionaryPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // The dictionary is a public tool, allow guests to use it!
    // No redirect needed.
  }, [user, router]);

  useEffect(() => {
    const fetchResults = async () => {
      if (query.trim().length < 2) {
        setResults([]);
        return;
      }
      
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:8004/dictionary?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        setResults(data.results || []);
      } catch (err) {
        console.error("Failed to fetch dictionary results", err);
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(fetchResults, 300); // 300ms debounce
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <SidebarLayout
      pageTitle="Ingredient Dictionary"
      pageSubtitle="Search through thousands of standardized ingredients, natural sources, and chemical additives."
    >
      <div className="flex flex-col w-full h-full">

        
        <div className="relative mb-8">
          <input 
            type="text" 
            placeholder="Search for an ingredient (e.g. Ascorbic Acid, E300, Soya)" 
            className="w-full p-4 pl-12 rounded-2xl border border-gray-200 focus:outline-none focus:border-brand focus:ring-2 focus:ring-brand/20 shadow-sm transition-all"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <svg className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </div>

        {loading && (
          <div className="text-center p-8 text-gray-400 animate-pulse">Searching databases...</div>
        )}

        {!loading && query.length >= 2 && results.length === 0 && (
          <div className="text-center p-12 bg-white rounded-2xl border border-gray-100 shadow-sm">
            <p className="text-gray-500 font-medium text-lg">No exact matches found.</p>
            <p className="text-sm text-gray-400 mt-2">Try searching for a simpler term or a broader category.</p>
          </div>
        )}

        <div className="space-y-3">
          {results.map((ingredient: any, i: number) => (
            <div key={i} className="flex flex-col md:flex-row md:items-start justify-between p-4 bg-white rounded-xl border border-gray-100 shadow-sm gap-4 transition-all hover:shadow-md">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-bold text-lg text-foreground capitalize truncate">{ingredient.name}</span>
                  {ingredient.code && <span className="text-xs text-gray-500 font-mono bg-gray-50 border border-gray-200 px-2 py-0.5 rounded shrink-0">{ingredient.code}</span>}
                </div>
                {ingredient.explanation && (
                  <p className="text-sm text-gray-500 leading-relaxed mb-1">{ingredient.explanation}</p>
                )}
              </div>
              <div className="flex flex-col sm:flex-row items-center gap-2 shrink-0 md:pt-1">
                <span className="w-full sm:w-[130px] text-[10px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-3 py-1.5 rounded-full text-center shrink-0">{ingredient.source}</span>
                <span className="w-full sm:w-[150px] text-[10px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-3 py-1.5 rounded-full text-center shrink-0">{ingredient.category}</span>
                <span className={`w-full sm:w-[100px] text-[10px] uppercase font-bold tracking-widest px-3 py-1.5 rounded-full text-center shrink-0 ${
                  ingredient.risk_level.toLowerCase() === 'safe' ? 'bg-green-100 text-green-700 border border-green-200' :
                  ingredient.risk_level.toLowerCase() === 'moderate risk' || ingredient.risk_level.toLowerCase() === 'permitted additive' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                  ingredient.risk_level.toLowerCase() === 'unknown' ? 'bg-gray-100 text-gray-600 border border-gray-200' :
                  'bg-red-100 text-red-700 border border-red-200'
                }`}>
                  {ingredient.risk_level}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </SidebarLayout>
  );
}
