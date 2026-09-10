"use client";
import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { signOut } from "firebase/auth";
import { auth } from "@/lib/firebase/firebase";
import { useRouter } from "next/navigation";

export default function AvatarMenu() {
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const router = useRouter();
  
  const displayName = user?.email?.split("@")[0] || "G";

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSignOut = async () => {
    setMenuOpen(false);
    await signOut(auth);
    router.push("/");
  };

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setMenuOpen(!menuOpen)}
        className="w-9 h-9 rounded-lg bg-white/15 text-white flex items-center justify-center text-xs font-bold uppercase hover:bg-white/25 active:scale-95 transition-all duration-200 focus:outline-none ring-1 ring-white/10"
      >
        {user ? displayName[0] : "G"}
      </button>

      {menuOpen && (
        <div className="absolute right-0 mt-3 w-56 bg-white rounded-2xl shadow-xl border border-gray-100 py-1.5 overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
          
          {user && (
            <div className="px-4 py-3 border-b border-gray-100">
              <p className="text-xs font-bold text-gray-900 truncate">{user.email?.split("@")[0]}</p>
              <p className="text-[10px] text-gray-400 truncate mt-0.5">{user.email}</p>
            </div>
          )}

          {!user ? (
            <Link href="/auth" onClick={() => setMenuOpen(false)}>
              <div className="px-4 py-2.5 text-sm text-brand font-medium hover:bg-brand/5 flex items-center gap-2.5 cursor-pointer transition-colors mx-1.5 rounded-lg">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" /></svg>
                Login / Sign Up
              </div>
            </Link>
          ) : (
            <>
              <Link href="/profile" onClick={() => setMenuOpen(false)}>
                <div className="px-4 py-2.5 text-sm text-gray-600 font-medium hover:bg-gray-50 hover:text-gray-900 flex items-center gap-2.5 cursor-pointer transition-colors mx-1.5 rounded-lg">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                  Profile Settings
                </div>
              </Link>
              <div className="h-px bg-gray-100 my-1" />
              <button 
                onClick={handleSignOut}
                className="w-full text-left px-4 py-2.5 text-sm text-red-500 font-medium hover:bg-red-50 hover:text-red-600 flex items-center gap-2.5 cursor-pointer transition-colors mx-1.5 rounded-lg"
                style={{ width: 'calc(100% - 12px)' }}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                Log Out
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
