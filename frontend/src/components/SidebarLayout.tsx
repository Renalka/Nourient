"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import AvatarMenu from './AvatarMenu';

interface SidebarLayoutProps {
  children: React.ReactNode;
  headerContent?: React.ReactNode;
}

export default function SidebarLayout({ children, headerContent }: SidebarLayoutProps) {
  const pathname = usePathname();
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const displayName = user?.email?.split('@')[0] || "U";

  const navItems = [
    { name: 'Overview', path: '/dashboard', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' },
    { name: 'Scan', path: '/scanner', icon: 'M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z' },
    { name: 'Dictionary', path: '/dictionary', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
    { name: 'Basket', path: '/basket', icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z' },
    { name: 'Methodology', path: '/methodology', icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
  ];

  return (
    <div className="flex h-screen bg-background font-sans text-foreground">
      
      {/* Off-canvas Left Pane (Drawer) */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out shadow-2xl ${menuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex flex-col h-full justify-between">
          <div>
            <div className="p-6 flex justify-between items-center border-b border-gray-100">
              <span className="font-bold tracking-widest text-xs text-gray-400 uppercase">Navigation</span>
              <button onClick={() => setMenuOpen(false)} className="text-gray-400 hover:text-gray-600 focus:outline-none bg-gray-50 hover:bg-gray-100 p-1 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            
            <nav className="mt-4 px-4 space-y-2">
              {navItems.map((item) => {
                const isActive = pathname === item.path;
                return (
                  <Link key={item.name} href={item.path} onClick={() => setMenuOpen(false)}>
                    <span className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                      isActive ? 'bg-brand text-white shadow-sm' : 'text-gray-500 hover:bg-gray-50 hover:text-brand'
                    }`}>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} /></svg>
                      {item.name}
                    </span>
                  </Link>
                );
              })}
            </nav>
          </div>
          
          <div className="p-6">
            <div className="p-4 bg-brand-light rounded-xl border border-brand/10">
              <h4 className="text-xs font-bold text-brand uppercase tracking-widest mb-1">Pro Plan</h4>
              <p className="text-[10px] text-gray-500 mb-3">Renews on 12 May, 2026</p>
              <button className="w-full py-2 bg-white text-brand text-xs font-bold rounded-lg border border-brand/20 hover:bg-gray-50 transition-colors">Manage Plan</button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 bg-background relative flex flex-col h-screen overflow-hidden">
        
        {/* Global Enforced Top Bar (Static/Fixed) */}
        <header className="border-b border-gray-200 bg-white px-4 md:px-8 py-3 flex justify-between items-center shrink-0 z-40 shadow-sm relative">
           
           {/* Left Section: Hamburger + Logo */}
           <div className="flex items-center gap-3 md:gap-6 lg:w-1/3">
             <button onClick={() => setMenuOpen(true)} className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none">
               <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
             </button>
             
             <Link href="/" className="flex items-center gap-2">
               <img src="/icon.png" alt="Nourient Logo" className="w-8 h-8 object-contain" />
               <span className="font-bold tracking-widest text-sm text-brand uppercase hidden md:block">Nourient</span>
             </Link>
           </div>
           
           {/* Center Section: Navigation Links (Desktop) */}
           <div className="hidden lg:flex flex-1 justify-center gap-2">
             {navItems.map(item => {
               const isActive = pathname === item.path;
               return (
                 <Link key={item.name} href={item.path}>
                   <span className={`px-5 py-2 rounded-full text-xs font-bold transition-colors ${
                     isActive ? 'bg-brand-light text-brand' : 'text-gray-500 hover:bg-gray-50 hover:text-foreground'
                   }`}>
                     {item.name}
                   </span>
                 </Link>
               );
             })}
           </div>

           {/* Mobile Center (headerContent) */}
           <div className="lg:hidden flex-1 flex justify-center overflow-hidden px-2">
             {headerContent}
           </div>
           
           {/* Right Section: HeaderContent (Desktop) + Avatar */}
           <div className="flex items-center justify-end gap-4 lg:w-1/3">
             <div className="hidden lg:block shrink-0">
               {headerContent}
             </div>
             <div className="shrink-0">
               <AvatarMenu />
             </div>
           </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>

        {/* Overlay when drawer is open */}
        {menuOpen && (
          <div 
            className="fixed inset-0 bg-gray-900/20 backdrop-blur-sm z-40 transition-opacity"
            onClick={() => setMenuOpen(false)}
          ></div>
        )}
      </main>
    </div>
  );
}
