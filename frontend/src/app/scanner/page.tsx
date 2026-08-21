'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import AuthWidget from "@/components/AuthWidget";
import { useAuth } from "@/context/AuthContext";

export default function Home() {
  const { user, getToken } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [score, setScore] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [detective, setDetective] = useState<any>(null);
  const [bioContext, setBioContext] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setScore(null);
      setAudit(null);
      setDetective(null);
      setBioContext(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setStatusText('Orchestrating microservices...');

    try {
      // 1. Get secure JWT from Firebase if logged in
      const token = await getToken();
      
      const formData = new FormData();
      formData.append('file', file);

      // 2. Call the Orchestrator backend
      const headers: HeadersInit = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const orchestratorResponse = await fetch('http://localhost:8003/api/v1/orchestrate/scan', {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!orchestratorResponse.ok) {
        if (orchestratorResponse.status === 401) {
          throw new Error("401 Unauthorized: Your token is invalid or expired.");
        }
        const errorText = await orchestratorResponse.text();
        throw new Error(`Orchestration failed: ${errorText}`);
      }

      const unifiedData = await orchestratorResponse.json();
      
      setResult(unifiedData.extracted_data);
      setScore(unifiedData.score);
      setAudit(unifiedData.audit);
      setDetective(unifiedData.detective);
      setBioContext(unifiedData.biocontext);

    } catch (err: any) {
      setError(err.message || 'An error occurred during orchestration.');
    } finally {
      setLoading(false);
      setStatusText('');
    }
  };

  return (
    <main className="min-h-screen p-6 md:p-12 bg-white text-black font-sans selection:bg-black selection:text-white">
      <div className="max-w-3xl mx-auto space-y-12">
        <header className="border-b border-black pb-6 relative">
          <Link href="/dashboard" className="absolute top-0 right-0 text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black hover:underline underline-offset-4">
            &larr; Dashboard
          </Link>
          <h1 className="text-3xl font-bold tracking-tighter uppercase">Vision Scanner</h1>
          <p className="mt-2 text-sm text-gray-500 uppercase tracking-widest">Personalized Intelligence Module</p>
          
          <div className="mt-6">
            <AuthWidget />
          </div>
        </header>

        <section className="space-y-6">
          <div className="space-y-2">
            <label className="block text-xs font-bold uppercase tracking-widest text-black">
              Analyze Label
            </label>
            <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-900 border border-black p-2 cursor-pointer focus:outline-none file:hidden"
              />
              <button
                onClick={handleUpload}
                disabled={!file || loading}
                className="w-full md:w-auto px-8 py-2.5 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Processing...' : 'Scan'}
              </button>
            </div>
            
            {loading && statusText && (
              <div className="mt-4 text-xs font-bold uppercase tracking-widest text-gray-500 animate-pulse">
                &gt; {statusText}
              </div>
            )}

            {error && (
              <div className="p-4 bg-black text-white text-sm mt-4 font-mono">
                [ERROR] {error}
              </div>
            )}
          </div>
        </section>

        {result && score && (
          <section className="border-t border-black pt-8 space-y-10 animate-in fade-in duration-500">
            
            {/* New: BioContext Personalization Section */}
            {bioContext ? (
              <div className="bg-black text-white p-6">
                <div className="flex justify-between items-center border-b border-gray-700 pb-4 mb-4">
                  <div>
                    <h2 className="text-sm font-bold uppercase tracking-widest text-gray-400">BioContext Profile</h2>
                    <p className="text-xl font-bold tracking-tighter uppercase">{bioContext.health_profile}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-xs text-gray-400 uppercase tracking-widest block">Metabolic Fit</span>
                    <span className={`text-4xl font-bold ${bioContext.metabolic_fit_score < 40 ? 'text-red-500' : 'text-white'}`}>
                      {bioContext.metabolic_fit_score}<span className="text-sm text-gray-500">/100</span>
                    </span>
                  </div>
                </div>
                <p className="text-sm leading-relaxed">{bioContext.context_reasoning}</p>
              </div>
            ) : !user ? (
              <div className="border border-dashed border-gray-400 p-6 text-center bg-gray-50">
                <h3 className="text-sm font-bold uppercase tracking-widest text-gray-600 mb-2">Unlock BioContext Personalization</h3>
                <p className="text-xs text-gray-500">Sign in with Google to dynamically adjust scores based on your metabolic profile, allergies, and health goals.</p>
              </div>
            ) : null}

            {/* Existing: Generic Food Decision Profile */}
            <div className="border border-black p-6 bg-gray-50">
              <h2 className="text-sm font-bold uppercase tracking-widest mb-6 text-gray-500">Generic Base Score</h2>
              
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
                <div>
                  <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Recommendation</div>
                  <div className={`text-2xl font-bold tracking-tighter uppercase ${
                    score.overall_recommendation.includes('LIMIT') ? 'text-gray-500' : 'text-black'
                  }`}>
                    {score.overall_recommendation}
                  </div>
                </div>
                <div className="flex gap-8">
                  <div>
                    <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Nutrition</div>
                    <div className="text-2xl font-bold tracking-tighter">{score.nutritional_quality_score}<span className="text-sm font-normal text-gray-500">/100</span></div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Processing</div>
                    <div className="text-2xl font-bold tracking-tighter">{score.processing_score}<span className="text-sm font-normal text-gray-500">/100</span></div>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Why?</div>
                <p className="text-sm leading-relaxed font-medium">{score.reasoning}</p>
              </div>
            </div>

            {/* Extracted Data Section */}
            <div>
              <h2 className="text-3xl font-bold tracking-tighter mb-1">{result.name || 'UNKNOWN PRODUCT'}</h2>
              <p className="text-sm text-gray-500 uppercase tracking-widest">{result.brand || 'UNKNOWN BRAND'} — {result.category || 'UNCATEGORIZED'}</p>
            </div>

            {result.claims && result.claims.length > 0 && (
              <div>
                <h3 className="text-xs font-bold uppercase tracking-widest border-b border-gray-200 pb-2 mb-4">Marketing Claims</h3>
                <div className="flex flex-wrap gap-2">
                  {result.claims.map((claim: string, idx: number) => (
                    <span key={idx} className="px-3 py-1 bg-white text-black text-xs font-bold uppercase tracking-wider border border-black">
                      {claim}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* 4. Ingredient Detective Section */}
            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest border-b border-gray-200 pb-2 mb-4 flex justify-between items-end">
                <span>Ingredients</span>
                {detective?.flagged_ingredients?.length > 0 && (
                  <span className="text-[10px] bg-black text-white px-2 py-0.5">{detective.flagged_ingredients.length} FLAGGED</span>
                )}
              </h3>
              <p className="text-sm leading-relaxed text-black mb-4">
                {result.ingredients?.length > 0 ? result.ingredients.join(', ') : 'NO INGREDIENTS DETECTED.'}
              </p>
              
              {detective?.flagged_ingredients?.length > 0 && (
                <div className="space-y-2 mt-4">
                  {detective.flagged_ingredients.map((ing: any, i: number) => (
                    <div key={i} className="border-l-2 border-black pl-4 py-1">
                      <div className="flex justify-between items-baseline mb-1">
                        <span className="font-bold text-sm tracking-tighter uppercase">{ing.name}</span>
                        <span className="text-[10px] text-gray-500 uppercase tracking-widest">{ing.purpose}</span>
                      </div>
                      <p className="text-xs text-gray-600 mb-1">{ing.explanation}</p>
                      <span className="text-[9px] font-bold uppercase tracking-widest px-1.5 py-0.5 border border-gray-300">
                        {ing.confidence_tier}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest border-b border-gray-200 pb-2 mb-4">Nutrition Facts</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-black border border-black">
                {Object.entries(result.nutrition || {}).map(([key, value]: any) => {
                  if (!value) return null;
                  return (
                    <div key={key} className="p-4 bg-white flex flex-col justify-between">
                      <div className="text-xs text-gray-500 uppercase tracking-widest mb-2">{key.replace('_', ' ')}</div>
                      <div className="text-xl font-bold tracking-tighter">{value.amount} <span className="text-sm font-normal text-gray-500">{value.unit}</span></div>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>
        )}

        {/* 3. TrueLabel Auditor Component */}
        {audit && (
          <div className="border border-black p-6 space-y-6">
            <div className="flex justify-between items-center border-b border-black pb-4">
              <h2 className="text-xl font-bold tracking-tighter uppercase">TrueLabel Audit</h2>
              <div className="text-right">
                <span className="text-xs text-gray-500 uppercase tracking-widest block">Trust Score</span>
                <span className="text-2xl font-bold">{audit.overall_trust_score}/100</span>
              </div>
            </div>
            
            <div className="space-y-4">
              {audit.verdicts && audit.verdicts.length > 0 ? (
                audit.verdicts.map((v: any, i: number) => (
                  <div key={i} className="border border-gray-200 p-4 relative">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-sm tracking-tighter uppercase">{v.claim}</h3>
                      <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 border ${
                        v.status === 'DECEPTIVE' ? 'border-black bg-black text-white' :
                        v.status === 'MISLEADING' ? 'border-gray-500 text-gray-800 bg-gray-100' :
                        'border-gray-300 text-gray-500'
                      }`}>
                        {v.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{v.reasoning}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500 uppercase">No claims analyzed.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
