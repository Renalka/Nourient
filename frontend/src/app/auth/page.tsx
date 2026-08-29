"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import AuthWidget from "@/components/AuthWidget";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";

export default function AuthPage() {
  const { user } = useAuth();
  const router = useRouter();

  // If already logged in, push to dashboard
  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  return (
    <main className="min-h-screen flex flex-col justify-center items-center bg-background text-foreground font-sans p-6">
      <div className="w-full max-w-sm space-y-8 bg-white p-8 rounded-2xl border border-gray-100 shadow-xl">
        <header className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2 mb-4">
            <img src="/logo.png" alt="Nourient Logo" className="w-8 h-8 object-contain" />
            <span className="font-bold tracking-widest text-sm text-brand uppercase">Nourient</span>
          </Link>
          <h1 className="text-2xl font-serif text-brand">Welcome back</h1>
          <p className="text-sm text-gray-500">Sign in to sync your food profile</p>
        </header>

        <AuthWidget />

        <div className="pt-4 text-center border-t border-gray-100">
          <Link 
            href="/dashboard" 
            className="text-sm font-medium text-gray-400 hover:text-brand transition-colors"
          >
            Continue as Guest
          </Link>
        </div>
      </div>
    </main>
  );
}
