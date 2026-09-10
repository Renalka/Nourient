"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import AvatarMenu from './AvatarMenu';
import Breadcrumbs from './Breadcrumbs';

interface SidebarLayoutProps {
  children: React.ReactNode;
  pageTitle?: string;
  pageSubtitle?: string;
}

export default function SidebarLayout({ 
  children, 
  pageTitle,
  pageSubtitle
}: SidebarLayoutProps) {
  const pathname = usePathname();
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
    { name: 'Scan', path: '/scanner', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
    { name: 'Alternatives', path: '/alternatives', icon: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4' },
    { name: 'Basket', path: '/basket', icon: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z' },
    { name: 'Dictionary', path: '/dictionary', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
    { name: 'Methodology', path: '/methodology', icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
  ];

  return (
    <div className="flex h-screen bg-background font-sans text-foreground">
      
      {/* Off-canvas Left Pane (Drawer) */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 bg-white transform transition-transform duration-300 ease-in-out ${menuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex flex-col h-full">
          {/* Drawer Header */}
          <div className="p-6 bg-brand">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <img src="/icon.png" alt="Nourient" className="w-6 h-6 object-contain brightness-0 invert" />
                  <span className="font-medium tracking-[0.2em] text-[12px] text-white uppercase">Nourient</span>
                </div>
              </div>
              <button onClick={() => setMenuOpen(false)} className="text-white/40 hover:text-white transition-colors p-1 -mr-1 -mt-1">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
          </div>
          
          <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
            {navItems.map((item) => {
              const isActive = pathname === item.path;
              return (
                <Link key={item.name} href={item.path} onClick={() => setMenuOpen(false)}>
                  <span className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive 
                      ? 'bg-brand text-white shadow-md shadow-brand/20' 
                      : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
                  }`}>
                    <svg className="w-[18px] h-[18px] shrink-0" fill="none" stroke="currentColor" strokeWidth={isActive ? 2.5 : 1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d={item.icon} /></svg>
                    {item.name}
                  </span>
                </Link>
              );
            })}
          </nav>

          {/* Drawer Footer */}
          <div className="p-4 border-t border-gray-100">
            <p className="text-[10px] text-gray-300 text-center tracking-wider">© 2026 Nourient</p>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 bg-background relative flex flex-col h-screen overflow-hidden">
        
        {/* ── Top Bar ── */}
        <header className="sticky top-0 z-40">
          {/* Main bar */}
          <div className="bg-black border-b border-white/5">
            <div className="px-4 md:px-8 h-14 flex items-center justify-between">
               
               {/* Left: Hamburger + Logo */}
               <div className="flex items-center gap-4 shrink-0">
                 <button 
                   onClick={() => setMenuOpen(true)} 
                   className="lg:hidden p-2 -ml-2 text-white/50 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 focus:outline-none"
                 >
                   <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                   </svg>
                 </button>
                 
                 <Link href="/" className="flex items-center gap-3">
                   <img src="/icon.png" alt="Nourient" className="w-6 h-6 object-contain invert brightness-0" />
                   <span className="font-medium tracking-[0.2em] text-[12px] text-white uppercase hidden md:inline">Nourient</span>
                 </Link>

                 {/* Vertical divider */}
                 <div className="hidden lg:block w-px h-7 bg-white/10 ml-2" />
               </div>
               
               {/* Center: Navigation Links (Desktop) */}
               <nav className="hidden lg:flex items-center gap-0.5 flex-1 justify-center">
                 {navItems.map(item => {
                   const isActive = pathname === item.path;
                   return (
                     <Link key={item.name} href={item.path}>
                       <span className={`group relative flex items-center gap-2 px-4 py-2 rounded-lg text-[12px] font-semibold uppercase tracking-wider transition-all duration-200 ${
                         isActive 
                           ? 'text-white bg-white/10'
                           : 'text-white/40 hover:text-white/80 hover:bg-white/5'
                       }`}>
                         <svg className={`w-4 h-4 shrink-0 transition-colors ${isActive ? 'text-emerald-400' : 'text-white/25 group-hover:text-white/50'}`} fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                           <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
                         </svg>
                         {item.name}
                         {isActive && (
                           <span className="absolute -bottom-[11px] left-3 right-3 h-[2px] bg-emerald-400 rounded-full" />
                         )}
                       </span>
                     </Link>
                   );
                 })}
               </nav>
               
               {/* Right: Avatar only */}
               <div className="flex items-center justify-end shrink-0">
                 <AvatarMenu />
               </div>
            </div>
          </div>
          {/* Accent gradient line */}
          <div className="h-[2px] bg-gradient-to-r from-emerald-500/80 via-brand/40 to-transparent" />
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 md:p-8 mx-auto w-full max-w-5xl flex flex-col min-h-full">
            
            {/* Global Page Header */}
            <header className="mb-6 md:mb-8 space-y-4">
              <Breadcrumbs />
              
              {pageTitle && (
                <div>
                  <h1 className="text-3xl md:text-4xl font-serif text-brand mb-2">{pageTitle}</h1>
                  {pageSubtitle && <p className="text-sm text-gray-500">{pageSubtitle}</p>}
                </div>
              )}
            </header>

            {/* Page Content */}
            {children}
          </div>
        </div>

        {/* Overlay when drawer is open */}
        {menuOpen && (
          <div 
            className="fixed inset-0 bg-gray-900/30 backdrop-blur-sm z-40 transition-opacity"
            onClick={() => setMenuOpen(false)}
          />
        )}
      </main>
    </div>
  );
}
