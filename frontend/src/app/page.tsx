'use client';

import Link from 'next/link';
import { useEffect, useRef } from 'react';

export default function LandingPage() {

  // Scroll reveal observer
  const revealRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const els = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver(
      (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.12 }
    );
    els.forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  const features = [
    { icon: 'M3 8v-2a2 2 0 012-2h2m10 0h2a2 2 0 012 2v2m-14 10v2a2 2 0 002 2h2m10 0h2a2 2 0 002-2v-2m-3-4l-3-3m0 0l-3 3m3-3v6', title: 'AI-Powered OCR', desc: 'Vision AI extracts every chemical compound with exceptional accuracy.' },
    { icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z', title: 'Detective Engine', desc: 'Maps aliases to real chemical identities — no jargon, just clarity.' },
    { icon: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z', title: 'Origin Categorisation', desc: 'Natural, Natural-Derived, or Synthetic — know the true source.' },
    { icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z', title: 'Scientific Risk Score', desc: 'EFSA-based risk categorisation using ADI thresholds and toxicology data.' },
    { icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z', title: 'Ingredient Dictionary', desc: 'Search by name, alias, or E-number with blazing fast autocomplete.' },
    { icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z', title: 'Smart Basket', desc: 'Compare healthier whole-food alternatives and build better baskets.' },
  ];

  const tickerItems = [
    'OCR Scanner', 'E-Number Decoding', 'EFSA Risk Model', 'Ingredient Origins', 'Chemical Mapping', 'Smart Basket', 'Biocontextual AI', 'Synthetic Detection', '75,000+ Ingredients',
    'OCR Scanner', 'E-Number Decoding', 'EFSA Risk Model', 'Ingredient Origins', 'Chemical Mapping', 'Smart Basket', 'Biocontextual AI', 'Synthetic Detection', '75,000+ Ingredients',
  ];

  return (
    <div className="bg-black font-sans overflow-x-hidden" ref={revealRef}>

      {/* ── NAV ──────────────────────────────────────────────── */}
      <header className="fixed top-0 left-0 right-0 z-50 px-6 md:px-12 py-4 flex justify-between items-center bg-black/80 backdrop-blur-md border-b border-white/5">
        <Link href="/" className="flex items-center gap-3">
          <img src="/icon.png" alt="Nourient" className="w-6 h-6 object-contain invert brightness-0" />
          <span className="font-medium tracking-[0.2em] text-[12px] text-white uppercase">Nourient</span>
        </Link>
        <nav className="hidden lg:flex gap-8">
          {['How it works','Features','For everyone','Science'].map(l => (
            <Link key={l} href={`#${l.toLowerCase().replace(/ /g,'-')}`}>
              <span className="text-[13px] font-medium text-gray-400 hover:text-white transition-colors">{l}</span>
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-6">
          <Link href="/auth"><span className="text-[13px] text-gray-400 hover:text-white transition-colors">Log in</span></Link>
          <Link href="/auth">
            <button className="px-5 py-2 bg-white text-black rounded-full text-[13px] font-bold hover:bg-gray-100 transition-all hover:scale-105 active:scale-95">
              Get started
            </button>
          </Link>
        </div>
      </header>

      {/* ── HERO ─────────────────────────────────────────────── */}
      <section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-20">
        {/* Ambient glow blobs */}
        <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] rounded-full bg-white/[0.02] blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-white/[0.03] blur-[100px] pointer-events-none" />

        <div className="max-w-7xl mx-auto px-8 w-full grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          {/* Left text */}
          <div className="space-y-8 z-10">
            <p className="animate-fade-up text-[11px] font-bold tracking-[0.3em] text-gray-500 uppercase">Food Intelligence, Reimagined</p>
            <h1 className="animate-fade-up delay-100 text-[5rem] font-serif text-white leading-[1.05] tracking-tight">
              Know what&apos;s<br/>
              <em className="not-italic text-gray-500">really</em> in<br/>
              your food.
            </h1>
            <p className="animate-fade-up delay-200 text-gray-400 text-lg max-w-md leading-relaxed">
              AI-powered ingredient analysis with a scientific lens. Because you deserve clarity, not chemical jargon.
            </p>
            <div className="animate-fade-up delay-300 flex items-center gap-6 pt-2">
              <Link href="/auth">
                <button className="group px-8 py-4 bg-white text-black rounded-full font-bold text-base hover:bg-gray-100 transition-all hover:scale-105 active:scale-95 flex items-center gap-3 shadow-[0_0_40px_rgba(255,255,255,0.15)]">
                  Try a scan now
                  <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                </button>
              </Link>
              <span className="text-gray-600 text-sm flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                No signup required
              </span>
            </div>
          </div>

          {/* Right — bag + overlays */}
          <div className="relative h-[680px] flex items-center justify-center animate-fade-in delay-300">

            {/* Floating bag */}
            <div className="animate-float relative z-10 w-[420px]">
              <img src="/hero-bag.jpg" alt="Packaged Food Label" className="w-full h-auto object-contain drop-shadow-[0_40px_60px_rgba(255,255,255,0.06)]" />
              {/* Scan line sweeping over label */}
              <div className="scan-line" style={{ top: '30%' }} />
            </div>

            {/* Scanning pill */}
            <div className="absolute bottom-28 left-4 z-30 animate-fade-up delay-500 bg-black/70 backdrop-blur-xl border border-white/15 rounded-full py-3 px-5 flex items-center gap-3 shadow-xl">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse flex-shrink-0" />
              <span className="text-white text-[13px] font-medium">Scanning ingredients...</span>
            </div>

            {/* Result chip — top right */}
            <div className="absolute top-20 right-0 z-30 animate-slide-left delay-600 bg-black/70 backdrop-blur-xl border border-white/15 rounded-2xl p-4 shadow-xl w-52">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">Risk Assessment</p>
              <div className="space-y-1.5">
                {[['Natural','62%','bg-green-400'],['Synthetic','28%','bg-yellow-400'],['High Risk','10%','bg-red-400']].map(([label,pct,cls]) => (
                  <div key={label} className="flex items-center gap-2">
                    <div className={`h-1 rounded-full ${cls}`} style={{ width: pct }} />
                    <span className="text-[11px] text-gray-400">{label} {pct}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Corner brackets viewfinder */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[340px] h-[260px] pointer-events-none z-20">
              {/* TL */}
              <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-white/40 rounded-tl-lg" />
              {/* TR */}
              <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-white/40 rounded-tr-lg" />
              {/* BL */}
              <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-white/40 rounded-bl-lg" />
              {/* BR */}
              <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-white/40 rounded-br-lg" />
            </div>

          </div>
        </div>

        {/* Bottom fade bridge to next section */}
        <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-[#F9F9F7] to-transparent pointer-events-none" />
      </section>

      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-[#F9F9F7] py-5 border-y border-gray-200 overflow-hidden">
        <div className="marquee-track">
          {tickerItems.map((item, i) => (
            <span key={i} className="flex items-center gap-3 pr-10 text-[11px] font-bold uppercase tracking-[0.18em] text-gray-400">
              <span className="w-1 h-1 rounded-full bg-gray-300 flex-shrink-0" />
              {item}
            </span>
          ))}
        </div>
      </div>

      {/* ── REST OF CONTENT on white/off-white background ─────── */}
      <div className="bg-[#F9F9F7]">
        <div className="max-w-7xl mx-auto px-8 pb-40 flex flex-col gap-0">

          {/* ── HOW IT WORKS ─────────────────────────────────── */}
          <section id="how-it-works" className="pt-32">
            <div className="reveal text-center mb-16">
              <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-3">The process</p>
              <h2 className="text-4xl font-serif text-gray-900">Three steps to food clarity.</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { n:'01', title:'Snap a Photo', desc:'Take a picture of any ingredient label. Our Vision AI extracts every compound in seconds.', delay:'delay-100' },
                { n:'02', title:'AI Decodes',   desc:'Our dual-engine AI maps confusing aliases and E-numbers to their true chemical identities.', delay:'delay-300' },
                { n:'03', title:'Get Your Score',desc:'Receive an instant personalised risk assessment — clear, scientific, and actionable.', delay:'delay-500' },
              ].map(s => (
                <div key={s.n} className={`reveal ${s.delay} group relative bg-white rounded-3xl p-10 border border-gray-100 hover:border-gray-300 hover:shadow-[0_8px_40px_rgba(0,0,0,0.06)] transition-all duration-300`}>
                  <span className="text-[11px] font-bold tracking-[0.2em] text-gray-300 uppercase mb-6 block">{s.n}</span>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{s.title}</h3>
                  <p className="text-sm text-gray-500 leading-relaxed">{s.desc}</p>
                  {/* Animated bottom border on hover */}
                  <div className="absolute bottom-0 left-8 right-8 h-px bg-gray-900 scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left rounded-full" />
                </div>
              ))}
            </div>
          </section>

          {/* ── FEATURES ─────────────────────────────────────── */}
          <section id="features" className="pt-32">
            <div className="reveal text-center mb-16">
              <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-3">Features</p>
              <h2 className="text-4xl font-serif text-gray-900">Powerful tools. Built on science.</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-gray-200 rounded-3xl overflow-hidden border border-gray-200">
              {features.map((f, i) => (
                <div key={i} className="reveal bg-white p-10 hover:bg-gray-50 transition-colors duration-200 group">
                  <div className="w-10 h-10 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center mb-6 group-hover:border-gray-300 transition-colors">
                    <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={f.icon} />
                    </svg>
                  </div>
                  <h4 className="font-bold text-sm text-gray-900 mb-2">{f.title}</h4>
                  <p className="text-[12px] text-gray-500 leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* ── FOR EVERYONE ─────────────────────────────────── */}
          <section id="for-everyone" className="pt-32">
            <div className="reveal bg-white rounded-3xl border border-gray-100 overflow-hidden">
              <div className="grid grid-cols-1 md:grid-cols-2">
                {/* Image fills left half */}
                <div className="relative h-[420px] md:h-auto overflow-hidden">
                  <img src="/landing-everyone.jpeg" alt="For Everyone" className="w-full h-full object-cover" />
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/10 md:to-transparent" />
                </div>
                {/* Text right half */}
                <div className="p-12 md:p-16 flex flex-col justify-center">
                  <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-4">For everyone</p>
                  <h2 className="text-4xl font-serif text-gray-900 mb-6">Empowering<br/>everyone.</h2>
                  <p className="text-gray-500 leading-relaxed mb-8">
                    Whether you&apos;re a parent packing a lunchbox, an athlete prioritising clean fuel, or simply someone trying to eat cleaner — Nourient cuts through the marketing fluff.
                  </p>
                  <ul className="space-y-4">
                    {['Parents & Families','Athletes & Fitness Enthusiasts','Health-Conscious Individuals'].map(t => (
                      <li key={t} className="flex items-center gap-3 text-sm font-medium text-gray-700">
                        <span className="w-5 h-5 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                          <svg className="w-3 h-3 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" /></svg>
                        </span>
                        {t}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </section>

          {/* ── SCIENCE / STATS (dark card) ───────────────────── */}
          <section id="science" className="pt-24">
            <div className="reveal bg-[#0D0D0D] rounded-3xl overflow-hidden">
              <div className="grid grid-cols-1 lg:grid-cols-2">

                {/* Left — headline */}
                <div className="p-14 md:p-16 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-white/5">
                  <div>
                    <p className="text-[10px] font-bold tracking-[0.25em] text-gray-600 uppercase mb-6">The science</p>
                    <h2 className="text-4xl font-serif text-white leading-tight mb-6">
                      Transparent.<br/>Scientific.<br/>Trustworthy.
                    </h2>
                    <p className="text-gray-400 leading-relaxed text-sm max-w-sm">
                      Built on global ingredient databases and EFSA toxicology models — every score is grounded in published science.
                    </p>
                  </div>
                  <div className="mt-12">
                    <Link href="/methodology">
                      <button className="group flex items-center gap-3 text-white text-sm font-bold hover:gap-4 transition-all">
                        Read our methodology
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                      </button>
                    </Link>
                  </div>
                </div>

                {/* Right — stats grid */}
                <div className="grid grid-cols-2 divide-x divide-y divide-white/5">
                  {[
                    { value: '75k+',   label: 'Ingredients Mapped' },
                    { value: '2',      label: 'AI Scoring Engines' },
                    { value: 'EFSA',   label: 'Risk Model Standard' },
                    { value: '100%',   label: 'Science-Backed' },
                  ].map((s, i) => (
                    <div key={i} className="p-10 flex flex-col justify-end hover:bg-white/[0.02] transition-colors">
                      <span className="text-4xl font-serif text-white mb-2">{s.value}</span>
                      <span className="text-[11px] text-gray-600 uppercase tracking-wider">{s.label}</span>
                    </div>
                  ))}
                </div>

              </div>
            </div>
          </section>

          {/* ── FINAL CTA ─────────────────────────────────────── */}
          <section className="pt-24 pb-8">
            <div className="reveal bg-black rounded-3xl p-16 text-center relative overflow-hidden">
              {/* Glow blob */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="w-[500px] h-[500px] rounded-full bg-white/[0.03] blur-[100px]" />
              </div>
              <p className="text-[11px] font-bold tracking-[0.25em] text-gray-600 uppercase mb-6 relative z-10">Start today</p>
              <h2 className="text-5xl font-serif text-white mb-6 relative z-10">Read your labels.<br/><em className="not-italic text-gray-500">Finally.</em></h2>
              <p className="text-gray-400 mb-10 max-w-md mx-auto relative z-10">
                No subscription required. No account needed to start scanning. Just clarity.
              </p>
              <Link href="/auth" className="relative z-10">
                <button className="px-10 py-4 bg-white text-black rounded-full font-bold text-base hover:bg-gray-100 transition-all hover:scale-105 active:scale-95 shadow-[0_0_50px_rgba(255,255,255,0.2)]">
                  Try a scan now — it&apos;s free
                </button>
              </Link>
            </div>
          </section>

        </div>
      </div>

    </div>
  );
}
