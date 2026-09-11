"use client";
import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import SidebarLayout from '@/components/SidebarLayout';
import Breadcrumbs from '@/components/Breadcrumbs';
import { apiUrl } from '@/lib/api';

export default function BasketPage() {
  const { user, loading, getToken } = useAuth();
  const router = useRouter();
  
  const [basketItems, setBasketItems] = useState<any[]>([]);
  const [frequencies, setFrequencies] = useState<Record<number, string>>({});
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);

  const fetchBasket = async () => {
    if (!user) return;
    try {
      const token = await getToken();
      const res = await fetch(apiUrl('/api/v1/basket/analyze', 8007), {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to fetch basket");
      const data = await res.json();
      setBasketItems(data.items || []);
      
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
      const token = await getToken();
      await fetch(apiUrl('/api/v1/basket/clear', 8007), {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      fetchBasket();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const removeItem = async (index: number) => {
    if (!user) return;
    try {
      const token = await getToken();
      await fetch(apiUrl(`/api/v1/basket/remove/${index}`, 8007), {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
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
      pageTitle="Basket Intelligence"
      pageSubtitle="Analyze your dietary habits based on product processing and consumption frequency."
    >
      <div className="space-y-8 animate-fade-in pb-12">

        {error && (
          <div className="p-4 bg-zinc-900 text-white rounded-xl border border-zinc-800 text-sm font-medium">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="w-8 h-8 border-4 border-zinc-200 border-t-black rounded-full animate-spin"></div>
            <div className="text-sm font-medium tracking-widest uppercase text-zinc-400 animate-pulse">
              Computing Behavioral Matrix
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            
            {/* Warnings Section - High Contrast Brutalist Style */}
            {analysis.isHighRisk && (
              <div className="relative overflow-hidden bg-black text-white p-6 md:p-8 rounded-3xl shadow-2xl group">
                {/* Animated background element */}
                <div className="absolute -right-20 -top-20 w-64 h-64 bg-white/5 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
                
                <div className="relative z-10 flex flex-col md:flex-row gap-6 items-start md:items-center">
                  <div className="w-12 h-12 bg-white text-black rounded-full flex items-center justify-center shrink-0">
                    <svg className="w-6 h-6 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <div>
                    <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-white/50 mb-2">Epidemiological Risk Alert</h2>
                    <p className="text-sm md:text-base font-medium leading-relaxed max-w-3xl">
                      Based on your selected frequencies, <span className="font-bold border-b border-white border-dashed">{analysis.upfProportion.toFixed(1)}%</span> of your weekly servings consist of Ultra-Processed Foods (NOVA Group 4). Clinical studies suggest keeping this below 20% to mitigate long-term metabolic risks.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Aggregated Scores - B&W Aesthetic */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* Primary Habit Score Card */}
              <div className="col-span-1 md:col-span-2 bg-white p-8 rounded-3xl border border-zinc-200 shadow-sm flex flex-col md:flex-row gap-8 items-center justify-between group hover:border-black transition-colors duration-300">
                <div className="flex items-center gap-8">
                  <div className="relative w-32 h-32 flex items-center justify-center shrink-0">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      {/* Track */}
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#f4f4f5" strokeWidth="6" />
                      {/* Progress */}
                      <circle 
                        cx="50" cy="50" r="45" fill="none" stroke="black" strokeWidth="6" 
                        strokeDasharray="283" 
                        strokeDashoffset={283 - (283 * analysis.habitScore / 100)} 
                        strokeLinecap="round" 
                        className="transition-all duration-1500 ease-out" 
                      />
                    </svg>
                    <div className="absolute text-center flex flex-col items-center">
                      <span className="text-4xl font-serif font-bold text-black tracking-tighter leading-none group-hover:scale-110 transition-transform duration-500">
                        {Math.round(analysis.habitScore)}
                      </span>
                    </div>
                  </div>
                  <div>
                    <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 mb-2">Clinical Habit Score</h2>
                    <p className="text-sm text-zinc-500 max-w-sm leading-relaxed">
                      An index based on nutritional quality (FSA-NPS) and processing (NOVA), dynamically weighted by your actual consumption frequency.
                    </p>
                  </div>
                </div>
              </div>

              {/* Secondary Metrics */}
              <div className="col-span-1 flex flex-col gap-6">
                <div className="bg-white p-6 rounded-3xl border border-zinc-200 shadow-sm flex-1 flex flex-col justify-center hover:-translate-y-1 hover:shadow-md transition-all duration-300">
                  <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-400 mb-1">UPF Proportion</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-serif font-bold text-black tracking-tighter">{Math.round(analysis.upfProportion)}</span>
                    <span className="text-sm font-bold text-zinc-300">%</span>
                  </div>
                </div>
                <div className="bg-black p-6 rounded-3xl shadow-sm flex-1 flex flex-col justify-center group hover:-translate-y-1 hover:shadow-xl hover:shadow-black/20 transition-all duration-300">
                  <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-500 mb-1">Avg Quality (FSA)</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-serif font-bold text-white tracking-tighter group-hover:text-zinc-200 transition-colors">{Math.round(analysis.nutriAverage)}</span>
                    <span className="text-sm font-bold text-zinc-600">/100</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Frequency Matrix */}
            <div className="bg-white p-6 md:p-8 rounded-3xl border border-zinc-200 shadow-sm">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-4 border-b border-zinc-100 pb-6">
                <div>
                  <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 mb-2">Behavioral Matrix <span className="text-black bg-zinc-100 px-2 py-0.5 rounded-full ml-2">{basketItems.length} Items</span></h2>
                  <p className="text-sm text-zinc-500">Fine-tune your consumption frequency to see how it impacts your long-term health metrics.</p>
                </div>
                {basketItems.length > 0 && (
                  <button 
                    onClick={clearBasket} 
                    className="text-[11px] font-bold uppercase tracking-wider text-zinc-500 hover:text-black hover:bg-zinc-100 px-4 py-2 rounded-full transition-all active:scale-95"
                  >
                    Clear Basket
                  </button>
                )}
              </div>
              
              {basketItems.length === 0 ? (
                <div className="py-20 flex flex-col items-center justify-center text-center">
                  <div className="w-16 h-16 rounded-full bg-zinc-50 border border-zinc-200 flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-zinc-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                  </div>
                  <p className="text-sm font-medium text-zinc-400">Your basket is perfectly clean.<br/>Scan products to begin analysis.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {basketItems.map((item: any, idx: number) => {
                    const freq = frequencies[idx] || "weekly";
                    const recommendation = item.score?.overall_recommendation || "UNKNOWN";
                    return (
                      <div 
                        key={idx} 
                        className="p-4 rounded-2xl border border-zinc-100 bg-white flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 hover:border-black hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 group animate-card-enter"
                        style={{ animationDelay: `${idx * 50}ms` }}
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-3 mb-1.5 flex-wrap">
                            <h3 className="font-bold text-sm text-black truncate">{item.name || 'Unnamed Product'}</h3>
                            {item.source === 'off_alternative' ? (
                              <span className="shrink-0 bg-zinc-100 text-zinc-500 border border-zinc-200 text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full flex items-center gap-1">
                                <svg className="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg> Discovered
                              </span>
                            ) : (
                              <span className="shrink-0 bg-emerald-50 text-emerald-600 border border-emerald-100 text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full flex items-center gap-1">
                                <svg className="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg> Scanned
                              </span>
                            )}
                            {recommendation.includes("LIMIT") && (
                              <span className="shrink-0 bg-black text-white text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full">High Risk</span>
                            )}
                          </div>
                          <div className="text-[11px] font-medium tracking-wide text-zinc-400 uppercase flex items-center gap-2">
                            <span>Processing Score: <span className="text-zinc-900">{item.score?.processing_score || 50}</span>/100</span>
                          </div>
                        </div>

                        <div className="flex items-center gap-4 w-full lg:w-auto">
                          {/* Toggle Group */}
                          <div className="flex-1 lg:flex-none flex bg-zinc-100/80 p-1 rounded-xl">
                            {['daily', 'weekly', 'occasional'].map((option) => (
                              <button 
                                key={option}
                                onClick={() => handleFreqChange(idx, option as any)}
                                className={`flex-1 lg:w-24 py-2 text-[11px] font-bold uppercase tracking-wider rounded-lg transition-all duration-200 ${
                                  freq === option 
                                    ? 'bg-black text-white shadow-md scale-100' 
                                    : 'text-zinc-500 hover:text-black hover:bg-zinc-200/50 scale-95 hover:scale-100'
                                }`}
                              >
                                {option}
                              </button>
                            ))}
                          </div>
                          
                          {/* Delete Button */}
                          <button 
                            onClick={() => removeItem(idx)}
                            className="p-2.5 text-zinc-300 hover:text-white hover:bg-black rounded-xl transition-all duration-200 shrink-0 group/btn"
                            title="Remove item"
                          >
                            <svg className="w-4 h-4 group-hover/btn:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
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
