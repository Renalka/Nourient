'use client';

import SidebarLayout from '@/components/SidebarLayout';

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
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Step 1 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 1</span>
            <h3 className="font-bold text-gray-900 mb-3">Vision Extraction</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Optical Character Recognition isolates text from noisy environmental backgrounds. The raw string is parsed into a structured array, extracting distinct ingredients while resolving nested brackets.
            </p>
          </div>

          {/* Step 2 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 2</span>
            <h3 className="font-bold text-gray-900 mb-3">Detective Engine</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Ingredients undergo rigorous chemical mapping. Ambiguous names and E-numbers are passed through our 75,000+ vector database to extract toxicity levels, origins, and hidden metabolic disruptors.
            </p>
          </div>

          {/* Step 3 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 3</span>
            <h3 className="font-bold text-gray-900 mb-3">Predictive Scoring</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Our proprietary machine learning model analyzes a multi-dimensional nutritional profile—balancing macros against synthetic toxicity—to compute a highly accurate, composite UPF score (0-100).
            </p>
          </div>

          {/* Step 4 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 4</span>
            <h3 className="font-bold text-gray-900 mb-3">BioContext Profiling</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Scores are instantly personalized. A product&apos;s &quot;Metabolic Fit&quot; shifts dynamically based on user health profiles (e.g., heavily penalizing sodium for Hypertension, or sugar for Diabetics).
            </p>
          </div>

          {/* Step 5 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 5</span>
            <h3 className="font-bold text-gray-900 mb-3">TrueLabel Audit</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              Front-of-pack marketing claims are cross-examined against the chemical reality. If a product claims &quot;No Sugar Added&quot; but contains high-glycemic Maltodextrin, the auditor exposes the greenwashing.
            </p>
          </div>

          {/* Step 6 */}
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden group hover:border-brand transition-colors">
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-100 group-hover:bg-brand transition-colors"></div>
            <div className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mb-6 text-brand">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
            </div>
            <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase mb-2 block">Stage 6</span>
            <h3 className="font-bold text-gray-900 mb-3">Basket Intelligence</h3>
            <p className="text-xs text-gray-500 leading-relaxed">
              External taxonomy databases (like Open Food Facts) are piped through our proprietary scoring engine in real-time. This calculates cumulative metabolic load and discovers cleaner alternatives seamlessly.
            </p>
          </div>

        </div>
      </div>

      {/* Microservice Architecture Section */}
      <div className="mb-12">
        <h2 className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase mb-8">Microservice Architecture</h2>
        
        <div className="bg-[#0A100D] p-8 md:p-10 rounded-3xl border border-[#1A2620] shadow-xl relative overflow-hidden">
          {/* Subtle grid background */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:24px_24px]"></div>
          
          <p className="relative z-10 text-gray-400 text-sm leading-relaxed max-w-3xl mb-10">
            Nourient is powered by a high-performance distributed microservice architecture. Each specialized engine runs independently, orchestrated via a central routing layer to ensure low-latency nutritional intelligence.
          </p>

          <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            {[
              { id: '01', name: 'Orchestrator Layer', desc: 'Central routing layer managing multi-engine pipeline execution and data aggregation.', color: 'text-brand' },
              { id: '02', name: 'Vision / Extraction', desc: 'Interfaces with advanced multimodal intelligence to extract structured data from noisy physical labels.', color: 'text-blue-400' },
              { id: '03', name: 'Detective Engine', desc: 'Executes rapid dictionary lookups and deep chemical mapping against toxicological databases.', color: 'text-yellow-400' },
              { id: '04', name: 'Scoring Engine', desc: 'Executes our proprietary machine learning models for real-time UPF evaluation and metabolic scoring.', color: 'text-rose-400' },
              { id: '05', name: 'Alternatives Engine', desc: 'Manages resilient fallback taxonomies and integrates with open-source databases like Open Food Facts.', color: 'text-emerald-400' },
              { id: '06', name: 'Basket Engine', desc: 'Handles cloud synchronization, metabolic cumulative load analysis, and secure persistent storage.', color: 'text-purple-400' },
            ].map((service) => (
              <div key={service.id} className="flex flex-col p-5 bg-white/[0.03] border border-white/10 rounded-2xl hover:bg-white/[0.05] transition-colors">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`text-[10px] font-mono px-2 py-1 bg-white/5 rounded border border-white/10 ${service.color}`}>
                    {service.id}
                  </span>
                  <h4 className="font-bold text-sm text-gray-200">{service.name}</h4>
                </div>
                <p className="text-[11px] text-gray-500 leading-relaxed">
                  {service.desc}
                </p>
              </div>
            ))}
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
            Ingredients are classified strictly by their manufacturing origin, cutting through ambiguous marketing terms like &quot;all natural&quot;.
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
