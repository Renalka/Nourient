"use client";
import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import SidebarLayout from '@/components/SidebarLayout';
import Breadcrumbs from '@/components/Breadcrumbs';

export default function BasketPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  
  const [basketItems, setBasketItems] = useState<any[]>([]);
  // Store the user's expected daily intake (in grams) for each item index
  const [intakes, setIntakes] = useState<Record<number, number>>({});
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [frequencies, setFrequencies] = useState<Record<number, string>>({});

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);

  const fetchBasket = async () => {
    if (!user) return;
    try {
      const res = await fetch(`http://localhost:8007/api/v1/basket/analyze/${user.uid}`);
      if (!res.ok) throw new Error("Failed to fetch basket");
      const data = await res.json();
      setBasketItems(data.items || []);
      
      // Initialize frequencies
      const initialFreq: Record<number, string> = {};
      (data.items || []).forEach((_: any, idx: number) => {
        initialFreq[idx] = "weekly";
      });
      setFrequencies(initialFreq);
      setIsLoading(false);
    } catch (err: any) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      setIsLoading(true);
      fetchBasket();
    } else {
      setIsLoading(false);
    }
  }, [user]);

  const clearBasket = async () => {
    if (!user) return;
    try {
      await fetch(`http://localhost:8007/api/v1/basket/clear/${user.uid}`, { method: 'DELETE' });
      fetchBasket();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const removeItem = async (index: number) => {
    if (!user) return;
    try {
      await fetch(`http://localhost:8007/api/v1/basket/remove/${user.uid}/${index}`, { method: 'DELETE' });
      fetchBasket();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleFreqChange = (idx: number, val: string) => {
    setFrequencies(prev => ({ ...prev, [idx]: val }));
  };

  // Epidemiologically Grounded Behavioral Logic
  // Based on the NutriNet-Santé cohort methodology for UPF dietary proportion
  // and the FSA-NPS (Food Standards Agency) index.
  const calculateAnalysis = () => {
    // 1. Map subjective frequencies to statistical weekly servings
    const weeklyServingsMap: Record<string, number> = {
      "daily": 7.0,       // 1 serving/day
      "weekly": 2.0,      // ~2 servings/week
      "occasional": 0.5   // ~1 serving every 2 weeks
    };

    let totalWeeklyServings = 0;
    let upfServings = 0; // Servings of NOVA Group 4 (Ultra-Processed)
    let weightedNutriScore = 0; // Grounded in FSA-NPS 0-100 scale from backend
    let weightedNovaScore = 0; // Grounded in NOVA ML 0-100 scale from backend

    basketItems.forEach((item, idx) => {
      const freq = frequencies[idx] || "weekly";
      const servingsPerWeek = weeklyServingsMap[freq];
      
      // Use the actual AI Orchestrator scores, grounded in real product data
      // (Default to 50 if the ML model failed to score a specific product)
      const novaScore = item.score?.processing_score || 50; 
      const fsaScore = item.score?.nutritional_quality_score || 50;

      totalWeeklyServings += servingsPerWeek;
      weightedNovaScore += (novaScore * servingsPerWeek);
      weightedNutriScore += (fsaScore * servingsPerWeek);

      // Epidemiological threshold: NOVA score < 40 indicates Ultra-Processed Food (NOVA 4)
      if (novaScore < 40) {
        upfServings += servingsPerWeek;
      }
    });

    if (totalWeeklyServings === 0) return { upfProportion: 0, nutriAverage: 0, isHighRisk: false, habitScore: 0 };
    
    // 2. Calculate Dietary Proportion of UPF (Key metric in clinical studies)
    // Studies show >20% UPF proportion significantly increases metabolic risks
    const upfProportion = (upfServings / totalWeeklyServings) * 100;
    const isHighRisk = upfProportion > 20;

    // 3. True Weighted Averages based on the actual backend data models
    const nutriAverage = weightedNutriScore / totalWeeklyServings;
    const novaAverage = weightedNovaScore / totalWeeklyServings;
    
    // 4. Clinical Habit Score (0-100)
    // A 50/50 blend of nutritional quality (FSA) and processing quality (NOVA)
    const habitScore = Math.max(0, Math.min(100, (nutriAverage * 0.5) + (novaAverage * 0.5)));

    return { upfProportion, nutriAverage, isHighRisk, habitScore };
  };

  const analysis = calculateAnalysis();

  if (loading || !user) return null;

  return (
    <SidebarLayout
      headerContent={
        <div className="hidden sm:flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-gray-400">
          <svg className="w-4 h-4 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Behavioral Basket Intelligence
        </div>
      }
    >
      <div className="p-8 max-w-5xl mx-auto space-y-8 animate-fade-in">
        <Breadcrumbs />
        <header className="mb-8 flex justify-between items-end -mt-4">
          <div>
            <h1 className="text-3xl font-serif text-brand mb-2">Basket Intelligence</h1>
            <p className="text-sm text-gray-500">Analyze your dietary habits based on product processing and consumption frequency.</p>
          </div>
        </header>

        {error && (
          <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 text-sm font-medium">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="text-sm font-medium text-gray-400 animate-pulse py-8">
            Analyzing basket habits...
          </div>
        ) : (
          <div className="space-y-8">
            {/* Warnings Section */}
            {analysis.isHighRisk && (
              <div className="border border-red-100 p-6 bg-red-50 rounded-2xl space-y-4 shadow-sm">
                <h2 className="text-xs font-bold uppercase tracking-widest text-red-700">Epidemiological Risk Alert</h2>
                <div className="bg-white border border-red-100 rounded-xl p-4 text-sm font-medium text-red-600 flex items-start gap-3">
                   <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                   Based on your selected frequencies, {analysis.upfProportion.toFixed(1)}% of your weekly servings consist of Ultra-Processed Foods (NOVA Group 4). Clinical studies suggest keeping this below 20% to mitigate long-term metabolic risks.
                </div>
              </div>
            )}

            {/* Aggregated Scores */}
            <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col md:flex-row gap-8 items-center justify-between">
              
              <div className="flex items-center gap-6">
                <div className="relative w-24 h-24 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#f3f4f6" strokeWidth="8" />
                    <circle cx="50" cy="50" r="45" fill="none" stroke={analysis.habitScore > 70 ? "#22c55e" : analysis.habitScore > 40 ? "#eab308" : "#ef4444"} strokeWidth="8" strokeDasharray="283" strokeDashoffset={283 - (283 * analysis.habitScore / 100)} strokeLinecap="round" className="transition-all duration-1000" />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center">
                    <span className="text-2xl font-serif text-foreground leading-none">{Math.round(analysis.habitScore)}</span>
                  </div>
                </div>
                <div>
                  <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">Clinical Habit Score</h2>
                  <p className="text-sm text-gray-500 max-w-xs">An index based on the FSA-NPS (nutritional quality) and NOVA (processing) standards, weighted by your consumption frequency.</p>
                </div>
              </div>

              <div className="flex gap-8 w-full md:w-auto">
                <div className="flex flex-col">
                  <span className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">UPF Proportion</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-serif text-foreground">{Math.round(analysis.upfProportion)}</span>
                    <span className="text-sm font-sans text-gray-400">%</span>
                  </div>
                </div>
                <div className="w-px h-12 bg-gray-100"></div>
                <div className="flex flex-col">
                  <span className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">Avg Quality (FSA)</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-serif text-foreground">{Math.round(analysis.nutriAverage)}</span>
                    <span className="text-sm font-sans text-gray-400">/100</span>
                  </div>
                </div>
              </div>

            </div>

            {/* Frequency Matrix */}
            <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
              <div className="flex justify-between items-center mb-8">
                <div>
                  <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">Behavioral Matrix ({basketItems.length})</h2>
                  <p className="text-sm text-gray-500">How often do you consume these products?</p>
                </div>
                {basketItems.length > 0 && (
                  <button onClick={clearBasket} className="text-xs font-medium text-red-500 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-colors">
                    Clear Basket
                  </button>
                )}
              </div>
              
              {basketItems.length === 0 ? (
                <div className="py-12 border-2 border-dashed border-gray-100 rounded-xl text-center">
                  <p className="text-sm text-gray-400">Your basket is empty. Scan products and add them to your basket.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {basketItems.map((item: any, idx: number) => {
                    const freq = frequencies[idx] || "weekly";
                    const recommendation = item.score?.overall_recommendation || "UNKNOWN";
                    return (
                      <div key={idx} className="p-4 rounded-2xl border border-gray-100 bg-gray-50/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:bg-white hover:shadow-sm transition-all group">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="font-bold text-sm text-foreground">{item.name || 'Unnamed Product'}</h3>
                            {recommendation.includes("LIMIT") && (
                              <span className="bg-red-100 text-red-700 text-[8px] font-bold uppercase tracking-widest px-2 py-0.5 rounded">Red Flag</span>
                            )}
                          </div>
                          <div className="text-xs text-gray-500 flex items-center gap-2">
                            <span>Processing Score: {item.score?.processing_score || 50}/100</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 w-full md:w-auto">
                          <div className="flex-1 md:flex-none flex bg-gray-100/50 p-1 rounded-xl border border-gray-200/50">
                            <button 
                              onClick={() => handleFreqChange(idx, "daily")}
                              className={`flex-1 md:w-24 py-1.5 text-xs font-bold rounded-lg transition-colors ${freq === 'daily' ? 'bg-white shadow-sm text-foreground' : 'text-gray-400 hover:text-gray-600'}`}
                            >
                              Daily
                            </button>
                            <button 
                              onClick={() => handleFreqChange(idx, "weekly")}
                              className={`flex-1 md:w-24 py-1.5 text-xs font-bold rounded-lg transition-colors ${freq === 'weekly' ? 'bg-white shadow-sm text-foreground' : 'text-gray-400 hover:text-gray-600'}`}
                            >
                              Weekly
                            </button>
                            <button 
                              onClick={() => handleFreqChange(idx, "occasional")}
                              className={`flex-1 md:w-28 py-1.5 text-xs font-bold rounded-lg transition-colors ${freq === 'occasional' ? 'bg-white shadow-sm text-foreground' : 'text-gray-400 hover:text-gray-600'}`}
                            >
                              Occasional
                            </button>
                          </div>
                          <button 
                            onClick={() => removeItem(idx)}
                            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-100 shrink-0"
                            title="Remove item"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </SidebarLayout>
  );
}
