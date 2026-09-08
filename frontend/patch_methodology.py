import re

with open('src/app/methodology/page.tsx', 'r') as f:
    content = f.read()

new_content = """'use client';

import SidebarLayout from '@/components/SidebarLayout';
import Link from 'next/link';

export default function MethodologyPage() {
  return (
    <SidebarLayout>
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl bg-[#0F1D15] text-white p-8 md:p-12 mb-8">
        <div className="absolute inset-0 bg-[url('/assets/bg/ai_lab.jpg')] opacity-20 bg-cover bg-center mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-[#0F1D15] via-[#0F1D15]/90 to-transparent"></div>
        <div className="relative z-10 max-w-2xl">
          <span className="inline-block px-3 py-1 bg-white/10 text-white text-[10px] font-bold tracking-widest uppercase rounded-full mb-6 border border-white/20">
            Scientific Protocol
          </span>
          <h1 className="text-3xl md:text-5xl font-serif mb-6 leading-tight">
            Decoding food complexity.<br />
            <span className="text-gray-400">Powered by data.</span>
          </h1>
          <p className="text-gray-300 text-sm md:text-base leading-relaxed max-w-xl">
            Nourient operates on a proprietary multi-stage intelligence pipeline. 
            We bridge the gap between chaotic marketing labels and strict toxicological frameworks—merging 
            advanced language models with deterministic scientific databases.
          </p>
        </div>
      </div>

      {/* The Pipeline */}
      <div className="mb-12">
        <h2 className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase mb-8">The Intelligence Pipeline</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          
          {/* Step 1 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 1</span>
            <h3 className="font-bold text-gray-900 mb-3">Vision Extraction</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Optical Character Recognition (OCR) isolates text from noisy environmental backgrounds. The raw string is parsed into a structured ingredient array, handling nested brackets and complex formulations.
            </p>
          </div>

          {/* Step 2 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 2</span>
            <h3 className="font-bold text-gray-900 mb-3">Semantic Decoding</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Ingredients are normalized against our 75,000+ vector database. We use a hybrid approach: deterministic alias matching first, falling back to a cosine-similarity semantic search for highly modified chemical names.
            </p>
          </div>

          {/* Step 3 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 3</span>
            <h3 className="font-bold text-gray-900 mb-3">UPF Scoring</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              A trained regression model evaluates the formulation's Ultra-Processed Food (UPF) density. It weighs the ratio of whole foods against synthetics, assigning a composite score between 0 and 100.
            </p>
          </div>

          {/* Step 4 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 4</span>
            <h3 className="font-bold text-gray-900 mb-3">TrueLabel Audit</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Marketing claims are cross-examined against the chemical reality. If a product claims "No Sugar Added" but contains high-glycemic Maltodextrin, the auditor flags it as deceptive.
            </p>
          </div>

        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        
        {/* Toxicology Base */}
        <div className="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
          <h2 className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase mb-6">Risk & Toxicology</h2>
          <div className="space-y-6">
            <p className="text-sm text-gray-600 leading-relaxed mb-8">
              When evaluating additives, we reference documented toxicology reports regarding <strong>Acceptable Daily Intake (ADI)</strong> thresholds. Our risk flags are determined by comparing typical concentrations against these safety limits.
            </p>
            
            <div className="space-y-4">
              <div className="flex items-start gap-4 p-4 rounded-2xl bg-red-50 border border-red-100">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0"></div>
                <div>
                  <h4 className="text-xs font-bold text-red-900 uppercase tracking-widest mb-1">High / Moderate Risk</h4>
                  <p className="text-xs text-red-700 leading-relaxed">Indicates international safety evaluations have found credible risks of populations exceeding safe daily intake levels through normal consumption, or links to microbiome disruption.</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4 p-4 rounded-2xl bg-yellow-50 border border-yellow-100">
                <div className="w-2 h-2 rounded-full bg-yellow-500 mt-1.5 shrink-0"></div>
                <div>
                  <h4 className="text-xs font-bold text-yellow-900 uppercase tracking-widest mb-1">Permitted Additive</h4>
                  <p className="text-xs text-yellow-700 leading-relaxed">Legally recognized food additives where specific overexposure toxicity ratings are not flagged, but which offer no nutritional value and may cause sensitivities in some individuals.</p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 rounded-2xl bg-green-50 border border-green-100">
                <div className="w-2 h-2 rounded-full bg-green-500 mt-1.5 shrink-0"></div>
                <div>
                  <h4 className="text-xs font-bold text-green-900 uppercase tracking-widest mb-1">Safe / Whole Food</h4>
                  <p className="text-xs text-green-700 leading-relaxed">Scientific consensus determines no significant risk of overexposure. These are typically unaltered biological ingredients or highly benign natural derivatives.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Taxonomies */}
        <div className="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm flex flex-col">
          <h2 className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase mb-6">Origin Classification</h2>
          <p className="text-sm text-gray-600 leading-relaxed mb-8">
            Ingredients are classified strictly by their manufacturing origin, cutting through ambiguous marketing terms like "all natural".
          </p>

          <div className="grid grid-cols-1 gap-4 flex-1">
            <div className="p-5 border border-gray-100 rounded-2xl hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-[10px] font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded">01</span>
                <h4 className="font-bold text-sm text-gray-900">Natural (Whole)</h4>
              </div>
              <p className="text-xs text-gray-500 pl-11">Obtained from a biological source via physical extraction. Completely unaltered at the molecular level.</p>
            </div>
            
            <div className="p-5 border border-gray-100 rounded-2xl hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-[10px] font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded">02</span>
                <h4 className="font-bold text-sm text-gray-900">Natural-Derived</h4>
              </div>
              <p className="text-xs text-gray-500 pl-11">Sourced biologically but subjected to natural fermentation or enzymatic processes (e.g., Xanthan Gum).</p>
            </div>

            <div className="p-5 border border-gray-100 rounded-2xl hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-[10px] font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded">03</span>
                <h4 className="font-bold text-sm text-gray-900">Synthetic</h4>
              </div>
              <p className="text-xs text-gray-500 pl-11">Heavily synthesized or altered in a laboratory environment, even if it mimics a natural compound (e.g., Artificial Dyes, Aspartame).</p>
            </div>
          </div>
        </div>

      </div>

      <div className="p-6 bg-brand-light/30 rounded-2xl border border-brand/10 text-xs text-gray-500 leading-relaxed">
        <strong className="text-brand">Disclaimer:</strong> The algorithmic assessments and scientific data provided by Nourient are for educational and informational purposes only. The models rely on open-source taxonomies and statistical probability. It is not intended as a substitute for professional medical advice, diagnosis, or treatment.
      </div>

    </SidebarLayout>
  );
}
"""

with open('src/app/methodology/page.tsx', 'w') as f:
    f.write(new_content)
