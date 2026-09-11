"use client";
import React from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import SidebarLayout from '@/components/SidebarLayout';
import { apiUrl } from '@/lib/api';
import { getScanHistory, saveScanHistory, ScanItem } from "@/lib/firebase/history";

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const displayName = user?.email?.split('@')[0] || "Guest";

  const [recentScans, setRecentScans] = React.useState<ScanItem[]>([]);
  const [totalScans, setTotalScans] = React.useState(0);
  const [healthProfile, setHealthProfile] = React.useState("GENERAL");
  const [isEditingProfile, setIsEditingProfile] = React.useState(false);
  const [savingProfile, setSavingProfile] = React.useState(false);
  const [mounted, setMounted] = React.useState(false);
  const [editingScanId, setEditingScanId] = React.useState<string | null>(null);
  const [editNameValue, setEditNameValue] = React.useState("");

  React.useEffect(() => {
    if (!loading && !user) {
      window.location.href = "/auth";
    }
  }, [user, loading]);

  React.useEffect(() => {
    if (loading || !user) return;
    const loadData = async () => {
      try {
        const history = await getScanHistory(user.uid);
        setRecentScans(history);
        
        // Let totalScans be just the history length for simplicity, 
        // or we could store a separate counter in Firestore if needed.
        setTotalScans(history.length);
        
        const profileKey = `healthProfile_${user.uid}`;
        const profileStr = localStorage.getItem(profileKey);
        if (profileStr) setHealthProfile(profileStr);
        else setHealthProfile("GENERAL");
      } catch (e) {
        console.error(e);
      }
    };
    loadData();
    const t = setTimeout(() => setMounted(true), 80);
    return () => clearTimeout(t);
  }, [user, loading]);

  const handleSaveProfile = async (profile: string) => {
    setSavingProfile(true);
    try {
      setHealthProfile(profile);
      if (user) {
        localStorage.setItem(`healthProfile_${user.uid}`, profile);
        const token = await user.getIdToken();
        await fetch(apiUrl('/api/v1/biocontext/update_profile', 8005), {
           method: 'POST',
           headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
           body: JSON.stringify({ health_profile: profile })
        });
      }
    } catch (e) { console.error(e); }
    setSavingProfile(false);
    setIsEditingProfile(false);
  };

  const getGreeting = () => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 17) return "Good afternoon";
    return "Good evening";
  };

  const ingredientScans = recentScans.filter(s => !s.scanMode || s.scanMode === 'ingredients' || s.scanMode === 'enhanced');

  const avgScore = ingredientScans.length > 0
    ? Math.round(ingredientScans.reduce((a, s) => a + (s?.metabolic_fit_score ?? s?.score ?? 0), 0) / ingredientScans.length) : 0;
  const cleanCount = ingredientScans.filter(s => (s?.score || 0) >= 70).length;
  const scoreOffset = 283 - (283 * avgScore) / 100;

  const goalLabel = healthProfile === 'DIABETIC' ? 'Low Sugar · Glycemic Control'
    : healthProfile === 'HYPERTENSION' ? 'Low Sodium · Heart Health'
    : 'Balanced Diet · Optimal Health';

  const handleSaveScanName = async (id: string | number) => {
    setEditingScanId(null);
    const updatedName = editNameValue.trim();
    if (!updatedName) return;

    const updatedScans = recentScans.map(s => s.id === id ? { ...s, name: updatedName } : s);
    setRecentScans(updatedScans);
    if (user) {
        await saveScanHistory(user.uid, updatedScans);
    }
  };

  if (loading || !user) return null;

  return (
    <SidebarLayout
      pageTitle={`${getGreeting()}, ${displayName}`}
      pageSubtitle="Let's make better food choices today."
    >
      <div className="space-y-10 relative">
        
        {/* Ambient page-level glow blob */}
        <div className="absolute top-1/4 right-0 w-[500px] h-[500px] bg-brand/[0.03] blur-[100px] rounded-full pointer-events-none -z-10 mix-blend-multiply" />

        {/* ── HERO STATS STRIP (Realistic Background) ── */}
        <div
          className={`bg-black rounded-3xl overflow-hidden shadow-2xl transition-all duration-700 relative group ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          {/* Parallax/Animated Image Background */}
          <div className="absolute inset-0 bg-[url('/assets/bg/organic_leaf.jpg')] bg-cover bg-center opacity-40 mix-blend-overlay group-hover:scale-105 transition-transform duration-[20s] ease-linear" />
          <div className="absolute inset-0 bg-gradient-to-r from-black via-black/80 to-black/60" />

          <div className="relative z-10 grid grid-cols-1 lg:grid-cols-5">
            {/* Left: score ring + greeting */}
            <div className="lg:col-span-2 p-8 md:p-10 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-white/10 backdrop-blur-sm">
              <div>
                <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-4 drop-shadow-md">Metabolic Fit Score</p>
                <div className="flex items-center gap-6">
                  <div className="relative w-28 h-28 shrink-0">
                    <svg className="w-full h-full transform -rotate-90 drop-shadow-xl" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="6" />
                      <circle
                        cx="50" cy="50" r="45" fill="none" stroke="#ffffff" strokeWidth="6"
                        strokeDasharray="283"
                        strokeDashoffset={mounted ? scoreOffset : 283}
                        strokeLinecap="round"
                        className="transition-all duration-[1400ms] ease-out"
                        style={{ filter: 'drop-shadow(0 0 6px rgba(255,255,255,0.4))' }}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-3xl font-serif text-white">{avgScore}</span>
                      <span className="text-[9px] text-gray-400 uppercase tracking-wider">/100</span>
                    </div>
                  </div>
                  <div>
                    <p className="text-white font-bold text-lg mb-1 drop-shadow-md">Tailored Match</p>
                    <p className="text-gray-300 text-xs leading-relaxed drop-shadow-sm">Personalized BioContext across {recentScans.length || 0} scanned products</p>
                  </div>
                </div>
              </div>
              <div className="mt-8 pt-6 border-t border-white/10 flex items-center justify-between">
                <div>
                  <p className="text-[9px] text-gray-400 uppercase tracking-wider mb-1 drop-shadow-sm">Active BioContext Profile</p>
                  <p className="text-white text-sm font-medium drop-shadow-md">{goalLabel}</p>
                </div>
                <button
                  onClick={() => setIsEditingProfile(true)}
                  className="text-[11px] text-gray-300 hover:text-white transition-colors font-medium flex items-center gap-1.5 bg-white/5 hover:bg-white/10 px-3 py-1.5 rounded-full backdrop-blur-md"
                >
                  Edit
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
                </button>
              </div>
            </div>

            {/* Right: stats grid */}
            <div className="lg:col-span-3 grid grid-cols-2 lg:grid-cols-2 divide-x divide-y divide-white/10 backdrop-blur-[2px]">
              {[
                { value: String(totalScans), label: 'Products Scanned' },
                { value: String(cleanCount), label: 'Clean Products' },
                { value: String(ingredientScans.reduce((count, s) => {
                    const list = s.decoded_additives || s.ingredients || [];
                    return count + list.filter((i: any) => i.risk_level?.toLowerCase() === 'high risk' || i.risk_level?.toLowerCase() === 'high').length;
                }, 0)), label: 'Red-Flag Additives' },
                { value: ingredientScans.length > 0 ? `${Math.round((ingredientScans.filter(s => (s.processing_score ?? 100) < 40).length / ingredientScans.length) * 100)}%` : '0%', label: 'Ultra-Processed (UPF)' },
              ].map((s, i) => (
                <div
                  key={i}
                  className="p-6 md:p-8 flex flex-col justify-end hover:bg-white/[0.04] transition-colors relative overflow-hidden group/stat"
                >
                  <div className="absolute inset-0 bg-white opacity-0 group-hover/stat:opacity-5 transition-opacity duration-300" />
                  <span className="text-3xl font-serif text-white mb-1 drop-shadow-md">{s.value}</span>
                  <span className="text-[10px] text-gray-400 uppercase tracking-wider drop-shadow-sm">{s.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── QUICK ACTIONS (Bento with glowing hover effects) ── */}
        <div
          className={`transition-all duration-700 delay-150 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-4">Quick Actions</p>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-px bg-gray-200 rounded-3xl overflow-hidden border border-gray-200 shadow-sm relative">
            
            {[
              { label: 'Scan Product', desc: 'Analyze any ingredient label with AI.', href: '/scanner',
                icon: 'M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z' },
              { label: 'Dictionary', desc: 'Search 75,000+ ingredients by name or E-number.', href: '/dictionary',
                icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
              { label: 'Basket', desc: 'Track cumulative nutrition across products.', href: '/basket',
                icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z' },
              { label: 'Claims Audit', desc: 'Expose greenwashing on front-of-pack claims.', href: '/auditor',
                icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
            ].map((a, i) => (
              <Link key={i} href={a.href} className="group bg-white p-7 md:p-8 hover:bg-gray-50 transition-colors duration-200 relative overflow-hidden">
                {/* Floating animated radial gradient on hover */}
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(26,50,36,0.03),transparent_70%)] opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                
                <div className="relative z-10 w-10 h-10 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center mb-5 group-hover:border-brand/30 group-hover:bg-brand/5 group-hover:scale-110 transition-all duration-300 ease-out">
                  <svg className="w-5 h-5 text-gray-700 group-hover:text-brand transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={a.icon} />
                  </svg>
                </div>
                <h4 className="relative z-10 font-bold text-sm text-gray-900 mb-1.5">{a.label}</h4>
                <p className="relative z-10 text-[12px] text-gray-500 leading-relaxed">{a.desc}</p>
                {/* Animated bottom border on hover */}
                <div className="absolute bottom-0 left-6 right-6 h-px bg-brand scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left rounded-full shadow-[0_0_8px_rgba(26,50,36,0.5)]" />
              </Link>
            ))}
          </div>
        </div>

        {/* ── TODAY'S INSIGHT (Image-backed left accent) ── */}
        <div
          className={`transition-all duration-700 delay-300 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-5">
              {/* Left accent with image background */}
              <div className="md:col-span-2 p-10 flex flex-col justify-center relative overflow-hidden group">
                <div className="absolute inset-0 bg-[url('/landing-everyone.jpeg')] bg-cover bg-center opacity-40 mix-blend-multiply group-hover:scale-105 transition-transform duration-[10s] ease-linear" />
                <div className="absolute inset-0 bg-gradient-to-r from-brand to-brand/90 mix-blend-multiply" />
                <div className="absolute inset-0 bg-gradient-to-br from-brand/90 to-brand-dark/95" />
                
                <div className="absolute -bottom-24 -left-24 w-64 h-64 rounded-full bg-white/10 blur-[40px] pointer-events-none" />
                
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse shadow-[0_0_8px_rgba(74,222,128,0.8)]" />
                    <p className="text-[10px] font-bold tracking-[0.25em] text-white/70 uppercase">Insight</p>
                  </div>
                  <h3 className="text-2xl font-serif text-white leading-snug drop-shadow-md">
                    {recentScans.length > 0 ? 'Your latest scan' : 'Ready to scan'}
                  </h3>
                </div>
              </div>
              
              {/* Right content */}
              <div className="md:col-span-3 p-10 flex flex-col justify-center bg-white relative overflow-hidden">
                <div className="absolute -right-20 -top-20 w-64 h-64 rounded-full bg-brand/[0.02] pointer-events-none" />
                
                <p className="text-gray-500 text-sm leading-relaxed mb-6 relative z-10">
                  {recentScans.length > 0 && recentScans[0]
                    ? <>Your recently scanned product, <span className="text-gray-900 font-medium">{recentScans[0]?.name || 'Unknown'}</span>, scored <span className="text-gray-900 font-bold">{recentScans[0]?.score || 0}/100</span>. Want to find healthier alternatives?</>
                    : "Start scanning food products to unlock personalized dietary insights, risk assessments, and AI-powered alternatives."}
                </p>
                <Link href={recentScans.length > 0 ? "/alternatives" : "/scanner"} className="relative z-10 w-fit">
                  <button className="group flex items-center gap-2 text-brand text-sm font-bold hover:gap-3 transition-all">
                    {recentScans.length > 0 ? "Find alternatives" : "Start scanning"}
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                  </button>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* ── RECENT SCANS ── */}
        <div
          className={`transition-all duration-700 delay-[450ms] ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          <div className="flex justify-between items-center mb-5 relative z-10">
            <div>
              <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-1">Recent Scans</p>
              <p className="text-sm text-gray-500">{totalScans > 0 ? `${totalScans} product${totalScans > 1 ? 's' : ''} analyzed` : 'No products scanned yet'}</p>
            </div>
            {recentScans.length > 0 && (
              <Link href="/scanner" className="group flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-gray-200 text-sm font-bold text-gray-900 hover:border-gray-300 hover:shadow-sm transition-all">
                New scan
                <svg className="w-4 h-4 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
              </Link>
            )}
          </div>

          {recentScans.length === 0 ? (
            <div className="bg-white rounded-3xl border border-gray-100 p-16 text-center shadow-sm">
              <div className="w-16 h-16 rounded-2xl bg-gray-50 border border-gray-100 flex items-center justify-center mx-auto mb-6 relative">
                <div className="absolute inset-0 bg-brand/5 rounded-2xl animate-ping opacity-20" style={{ animationDuration: '3s' }} />
                <svg className="w-7 h-7 text-gray-400 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">No scans yet</h3>
              <p className="text-sm text-gray-500 max-w-sm mx-auto mb-8">Scan a product label to start building your food intelligence profile. Your history will appear here.</p>
              <Link href="/scanner">
                <button className="px-8 py-3 bg-[#0D0D0D] text-white rounded-full text-sm font-bold hover:bg-black transition-all hover:scale-105 active:scale-95 shadow-[0_4px_20px_rgba(0,0,0,0.12)]">
                  Scan your first product
                </button>
              </Link>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-gray-200 overflow-hidden divide-y divide-gray-100 shadow-sm">
              {recentScans.slice(0, 5).map((scan, i) => {
                if (!scan) return null;
                return (
                <div
                  key={scan.id || i}
                  className={`group relative p-5 md:px-8 md:py-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-brand/[0.02] transition-colors duration-300 ${
                    mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
                  }`}
                  style={{ transitionDelay: `${550 + i * 100}ms`, transitionDuration: '600ms' }}
                >
                  {/* Subtle left border highlight on hover */}
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-brand scale-y-0 group-hover:scale-y-100 origin-center transition-transform duration-300" />
                  
                  <div className="flex-1 min-w-0 z-10 pr-6">
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-3 min-w-0 group/edit">
                        {editingScanId === scan.id ? (
                          <input 
                             autoFocus
                             value={editNameValue}
                             onChange={(e) => setEditNameValue(e.target.value)}
                             onBlur={() => handleSaveScanName(scan.id)}
                             onKeyDown={(e) => e.key === 'Enter' && handleSaveScanName(scan.id)}
                             className="text-sm font-bold text-gray-900 border-b border-brand focus:outline-none bg-transparent w-full"
                          />
                        ) : (
                          <>
                            <h4 className="text-sm font-bold text-gray-900 truncate group-hover:text-brand transition-colors">{scan.name}</h4>
                            <button 
                               onClick={(e) => { 
                                 e.preventDefault();
                                 e.stopPropagation();
                                 setEditingScanId(scan.id); 
                                 setEditNameValue(scan.name); 
                               }} 
                               className="text-gray-300 hover:text-brand transition-colors opacity-0 group-hover/edit:opacity-100 shrink-0"
                            >
                               <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                            </button>
                          </>
                        )}
                      </div>
                      <span className="text-[10px] text-gray-400 bg-white px-2 py-0.5 rounded-full border border-gray-100 shrink-0 shadow-sm ml-4">
                        {new Date(scan.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 line-clamp-1">
                      {(scan.ingredients?.length || 0) > 0 ? scan.ingredients!.map((ing: any) => ing?.name || '').filter(Boolean).join(', ') : 'No ingredients detected'}
                    </p>
                  </div>
                  <div className="flex items-center justify-end gap-3 shrink-0 z-10 min-w-[140px]">
                    {scan.score === -1 && scan.processing_score === -1 ? (
                      <div className="text-center w-full">
                         <span className="text-xs font-bold text-gray-500 bg-gray-100 px-3 py-1 rounded-full border border-gray-200">{scan.scanMode === 'claims' ? 'Claims Check' : scan.scanMode === 'front' ? 'Front Label' : 'Nutrition Facts'}</span>
                      </div>
                    ) : (
                      <>
                        {scan.score !== -1 && (
                          <div className="text-center w-12">
                            <p className="text-[9px] text-gray-400 uppercase tracking-wider mb-0.5">{scan.primaryLabel || 'Nutri'}</p>
                            <span className={`text-lg font-serif font-bold ${
                              (scan.primaryLabel === 'Decept' && scan.score > 50) ? 'text-red-600' :
                              (scan.primaryLabel === 'Decept' && scan.score <= 50) ? 'text-green-600' :
                              scan.score >= 75 ? 'text-green-600' : 
                              scan.score >= 45 ? 'text-yellow-600' : 'text-red-600'
                            }`}>{scan.score}</span>
                          </div>
                        )}
                        {scan.processing_score !== undefined && scan.processing_score !== -1 && (
                          <>
                            {scan.score !== -1 && <div className="w-px h-8 bg-gray-200 group-hover:bg-gray-300 transition-colors" />}
                            <div className="text-center w-12">
                              <p className="text-[9px] text-gray-400 uppercase tracking-wider mb-0.5">{scan.secondaryLabel || 'AI'}</p>
                              <span className={`text-lg font-serif font-bold ${scan.processing_score >= 80 ? 'text-brand' : scan.processing_score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>{scan.processing_score}</span>
                            </div>
                          </>
                        )}
                      </>
                    )}
                  </div>
                </div>
              );})}
            </div>
          )}
        </div>

        {/* ── METHODOLOGY CTA (Realistic AI Lab image background) ── */}
        <div
          className={`transition-all duration-700 delay-[600ms] ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          <Link href="/methodology" className="block">
            <div className="bg-black rounded-3xl p-10 md:p-12 relative overflow-hidden group hover:shadow-[0_12px_40px_rgba(0,0,0,0.3)] transition-all duration-500">
              {/* Photographic Background */}
              <div className="absolute inset-0 bg-[url('/assets/bg/ai_lab.jpg')] bg-cover bg-center opacity-30 mix-blend-luminosity group-hover:scale-105 group-hover:opacity-40 transition-all duration-1000 ease-out" />
              <div className="absolute inset-0 bg-gradient-to-r from-black via-black/80 to-transparent" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
              
              {/* Scanning laser animation line */}
              <div className="absolute top-0 left-0 bottom-0 w-1 bg-brand/50 shadow-[0_0_20px_rgba(26,50,36,0.8)] opacity-0 group-hover:opacity-100 group-hover:animate-[ping_2s_linear_infinite]" style={{ animationDuration: '3s' }} />

              <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div>
                  <p className="text-[10px] font-bold tracking-[0.25em] text-white/50 uppercase mb-3 drop-shadow-md">Transparency</p>
                  <h3 className="text-2xl font-serif text-white leading-tight drop-shadow-lg">How our AI works.</h3>
                  <p className="text-gray-400 text-sm mt-2 max-w-md drop-shadow-sm">Read about EFSA risk models, dual-engine scoring, and ingredient origin classification.</p>
                </div>
                <button className="group flex items-center justify-center gap-3 bg-white/10 backdrop-blur-md border border-white/20 px-6 py-3 rounded-full text-white text-sm font-bold hover:bg-white hover:text-black transition-all shrink-0">
                  Read methodology
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                </button>
              </div>
            </div>
          </Link>
        </div>

      </div>

      {/* ── PROFILE EDIT MODAL ── */}
      {isEditingProfile && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md" onClick={() => setIsEditingProfile(false)}>
          <div className="bg-white rounded-3xl w-full max-w-md p-8 shadow-2xl animate-card-enter" onClick={e => e.stopPropagation()}>
            <p className="text-[10px] font-bold tracking-[0.25em] text-gray-400 uppercase mb-2">Settings</p>
            <h2 className="text-2xl font-serif text-gray-900 mb-2">Health Profile</h2>
            <p className="text-sm text-gray-500 mb-8">Select your primary health context. Nourient tailors risk assessments and scoring to your goals.</p>
            
            <div className="space-y-3 mb-8">
              {[
                { id: 'GENERAL', label: 'General Health', desc: 'Balanced diet and overall wellness', icon: '🌿' },
                { id: 'DIABETIC', label: 'Diabetic / Low Sugar', desc: 'Strict glycemic control, low added sugar', icon: '🩸' },
                { id: 'HYPERTENSION', label: 'Hypertension / Low Sodium', desc: 'Heart health, strict sodium limits', icon: '❤️' }
              ].map(opt => (
                <div
                  key={opt.id}
                  onClick={() => setHealthProfile(opt.id)}
                  className={`group relative p-5 rounded-2xl border-2 cursor-pointer transition-all duration-200 ${
                    healthProfile === opt.id
                      ? 'border-brand bg-brand-light/20'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="flex items-center gap-3">
                      <span className="text-lg">{opt.icon}</span>
                      <span className={`font-bold text-sm ${healthProfile === opt.id ? 'text-gray-900' : 'text-gray-700'}`}>{opt.label}</span>
                    </span>
                    {healthProfile === opt.id && (
                      <div className="w-5 h-5 rounded-full bg-brand flex items-center justify-center shadow-sm">
                        <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
                      </div>
                    )}
                  </div>
                  <span className="text-xs text-gray-500 ml-10">{opt.desc}</span>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setIsEditingProfile(false)}
                className="px-5 py-2.5 rounded-full text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleSaveProfile(healthProfile)}
                disabled={savingProfile}
                className="px-6 py-2.5 bg-[#0D0D0D] text-white rounded-full text-sm font-bold hover:bg-black disabled:opacity-50 transition-all hover:scale-105 active:scale-95 shadow-sm"
              >
                {savingProfile ? 'Saving...' : 'Save Profile'}
              </button>
            </div>
          </div>
        </div>
      )}
    </SidebarLayout>
  );
}
