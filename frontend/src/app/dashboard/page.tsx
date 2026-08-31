"use client";
import React from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import SidebarLayout from '@/components/SidebarLayout';
import AvatarMenu from '@/components/AvatarMenu';
import Breadcrumbs from '@/components/Breadcrumbs';

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const displayName = user?.email?.split('@')[0] || "Guest";

  const [recentScans, setRecentScans] = React.useState<any[]>([]);

  React.useEffect(() => {
    try {
      const historyStr = localStorage.getItem('recentScans');
      if (historyStr) {
        setRecentScans(JSON.parse(historyStr));
      }
    } catch (e) {
      console.error(e);
    }
  }, []);

  return (
    <SidebarLayout
      headerContent={
        <div className="hidden sm:flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-gray-400">
          <svg className="w-4 h-4 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          Overview
        </div>
      }
    >
      {loading ? (
        <div className="p-8 max-w-5xl mx-auto space-y-8 animate-pulse">
           <div className="h-10 bg-gray-200 rounded w-1/3 mb-2"></div>
           <div className="h-4 bg-gray-100 rounded w-1/4 mb-12"></div>
           <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
             <div className="lg:col-span-2 bg-gray-100 rounded-2xl h-80"></div>
             <div className="bg-gray-100 rounded-2xl h-80"></div>
           </div>
        </div>
      ) : (
      <div className="p-8 max-w-5xl mx-auto space-y-8 animate-fade-in">
        <Breadcrumbs />
        <header className="flex justify-between items-end -mt-4">
          <div>
            <h1 className="text-3xl font-serif text-brand mb-2">Good morning, {displayName}</h1>
            <p className="text-sm text-gray-500">Let's make better food choices today.</p>
          </div>
          <div className="hidden md:flex items-center gap-4">
             <div className="relative">
               <svg className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
               <input type="text" placeholder="Search products, brands..." className="pl-9 pr-4 py-2 bg-white border border-gray-200 rounded-full text-sm focus:outline-none focus:border-brand w-64" />
             </div>
             <AvatarMenu />
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Food Profile Card */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-gray-100 shadow-sm flex flex-col justify-between">
            <div className="flex justify-between items-start mb-6">
              <h2 className="font-bold text-foreground">Your Food Profile</h2>
              <button className="text-xs font-medium text-brand hover:underline">Edit goals &rarr;</button>
            </div>
            
            <div className="flex flex-col md:flex-row gap-8 items-center justify-center py-4">
              {/* Circular Score */}
              <div className="relative w-40 h-40 flex items-center justify-center">
                 {/* Fake SVG Circle */}
                 <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                   <circle cx="50" cy="50" r="45" fill="none" stroke="#E8F0EA" strokeWidth="8" />
                   <circle cx="50" cy="50" r="45" fill="none" stroke="#1A3224" strokeWidth="8" strokeDasharray="283" strokeDashoffset="79" strokeLinecap="round" />
                 </svg>
                 <div className="absolute text-center">
                   <div className="text-4xl font-serif text-brand">72</div>
                   <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">/100</div>
                 </div>
              </div>

              {/* Progress Bars */}
              <div className="flex-1 w-full space-y-4">
                {[
                  { label: "Nutri-Score FSA", value: 76 },
                  { label: "NOVA ML Score", value: 45 },
                  { label: "Protein Adequacy", value: 42 },
                  { label: "Added Sugar", value: 39 },
                ].map(stat => (
                  <div key={stat.label} className="flex items-center gap-4 text-xs font-medium">
                    <span className="w-32 text-gray-600">{stat.label}</span>
                    <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-brand rounded-full" style={{ width: `${stat.value}%` }}></div>
                    </div>
                    <span className="w-6 text-right text-foreground font-bold">{stat.value}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 grid grid-cols-2 gap-4">
               <div>
                 <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mb-1">Goal</p>
                 <p className="text-sm font-medium text-foreground">High Protein • Low Added Sugar</p>
               </div>
               <div>
                 <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mb-1">Context</p>
                 <p className="text-sm font-medium text-foreground">Moderate activity • 2,100 kcal/day</p>
               </div>
            </div>
          </div>

          {/* Right Column: Insight & Actions */}
          <div className="space-y-6">
            {/* Today's Insight */}
            <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm relative overflow-hidden h-48 flex flex-col justify-between">
               <div className="relative z-10 w-2/3">
                 <h2 className="font-bold text-foreground mb-2">Today's Insight</h2>
                 <p className="text-sm text-gray-600 leading-relaxed">Most cereals you scan tend to be high in added sugar.</p>
                 <button className="text-xs font-medium text-brand hover:underline mt-4">View details &rarr;</button>
               </div>
               {/* Decorative background shape replacing image */}
               <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-brand-light rounded-full opacity-50"></div>
            </div>
            <div className="min-w-[140px]">
              <Link href="/scanner" className="group block p-4 bg-white border border-gray-100 rounded-2xl hover:border-brand hover:shadow-md transition-all h-full">
                <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-3">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                </div>
                <h3 className="font-bold text-sm text-foreground mb-1 group-hover:text-blue-600 transition-colors">Label Audit</h3>
                <p className="text-[10px] text-gray-500">Verify front-of-pack claims</p>
              </Link>
            </div>

            <div className="min-w-[140px]">
              <div className="p-4 bg-gray-50 border border-gray-100 rounded-2xl h-full opacity-70 cursor-not-allowed flex flex-col justify-center items-center text-center">
                  <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 mb-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                  </div>
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Search<br/>Database</span>
              </div>
            </div>

            <div className="min-w-[140px]">
              <div className="h-full flex items-center justify-center">
                <Link href="/basket" className="group flex flex-col items-center justify-center w-24 h-24 rounded-full border-2 border-dashed border-gray-200 hover:border-brand hover:bg-brand/5 transition-all">
                  <div className="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-gray-600 group-hover:bg-white group-hover:text-brand mb-2 transition-colors shadow-sm">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                  </div>
                  <span className="text-[10px] font-medium text-center text-gray-600 group-hover:text-brand">Food<br/>Basket</span>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Scans */}
        <div className="pt-4">
          <div className="flex justify-between items-center mb-6">
            <h2 className="font-bold text-foreground">Recent Scans</h2>
            <button className="text-xs font-medium text-gray-500 hover:text-brand">View all &rarr;</button>
          </div>
          
          <div className="flex flex-col gap-3">
            {recentScans.length === 0 ? (
              <div className="p-8 bg-gray-50 border border-gray-100 rounded-2xl text-center">
                <p className="text-sm text-gray-500">No recent scans found.</p>
                <Link href="/scanner" className="text-brand font-bold text-sm mt-2 inline-block">Scan a product &rarr;</Link>
              </div>
            ) : (
              recentScans.map((scan, i) => (
                <div key={scan.id || i} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex flex-col">
                    <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                      {scan.name}
                      <span className="text-[10px] font-medium text-gray-400 bg-gray-50 px-2 py-0.5 rounded-full border border-gray-100">
                        {new Date(scan.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </h3>
                    <p className="text-xs text-gray-500 mt-1 line-clamp-1 max-w-2xl">
                      {scan.ingredients && scan.ingredients.length > 0 
                        ? scan.ingredients.map((ing: any) => ing.name).join(', ') 
                        : 'No ingredients detected'}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <div className="flex flex-col items-end">
                      <span className="text-[10px] uppercase font-bold text-gray-400 tracking-widest">Score</span>
                      <div className={`text-lg font-black ${scan.score > 75 ? 'text-green-600' : scan.score > 45 ? 'text-yellow-600' : 'text-red-600'}`}>
                        {scan.score}/100
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
      </div>
      )}
    </SidebarLayout>
  );
}
