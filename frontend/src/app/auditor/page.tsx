"use client";
import React, { useState } from 'react';
import { useAuth } from "@/context/AuthContext";
import SidebarLayout from '@/components/SidebarLayout';
import { apiUrl } from '@/lib/api';

export default function AuditorPage() {
  const { getToken } = useAuth();

  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusText, setStatusText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const [result, setResult] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setStatusText('Running TrueLabel AI Audit...');

    try {
      const token = await getToken();
      const formData = new FormData();
      formData.append('file', file);

      const headers: HeadersInit = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(apiUrl('/api/v1/orchestrate/auditor'), {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Audit failed: ${errorText}`);
        throw new Error('An unexpected server error occurred while running the audit. Please try again later.');
      }

      const data = await response.json();
      setResult(data.extracted_data);
      setAudit(data.audit);

    } catch (err: any) {
      setError(err.message || 'An error occurred during audit.');
    } finally {
      setIsLoading(false);
      setStatusText('');
    }
  };

  return (
    <SidebarLayout
      pageTitle="TrueLabel Auditor"
      pageSubtitle="Adversarial Marketing Analysis"
    >
      <div className="space-y-12">
        <section className="space-y-6">
          <div className="space-y-2">
            <label className="block text-xs font-bold uppercase tracking-widest text-black">
              Upload Product Label
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
                disabled={!file || isLoading}
                className="w-full md:w-auto px-8 py-2.5 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Auditing...' : 'Run Audit'}
              </button>
            </div>
            
            {isLoading && statusText && (
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

        {audit && (
          <section className="border-t border-black pt-8 space-y-10 animate-in fade-in duration-500">
            <div className="border border-black p-6 space-y-6">
              <div className="flex justify-between items-center border-b border-black pb-4">
                <h2 className="text-xl font-bold tracking-tighter uppercase">Greenwashing Verdict</h2>
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
          </section>
        )}
      </div>
    </SidebarLayout>
  );
}
