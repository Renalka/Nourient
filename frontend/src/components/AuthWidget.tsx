"use client";
import React, { useState } from "react";
import { signInWithPopup, GoogleAuthProvider, signOut } from "firebase/auth";
import { auth } from "@/lib/firebase/firebase";
import { useAuth } from "@/context/AuthContext";

export default function AuthWidget() {
  const { user, loading } = useAuth();
  const [error, setError] = useState("");

  const handleGoogleSignIn = async () => {
    try {
      setError("");
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
    } catch (err: any) {
      setError(err.message || "Failed to sign in");
    }
  };

  const handleSignOut = async () => {
    await signOut(auth);
  };

  if (loading) {
    return <div className="text-xs font-bold uppercase tracking-widest text-gray-400">Loading Auth...</div>;
  }

  if (user) {
    return (
      <div className="flex items-center gap-4 border border-black p-2 bg-gray-50">
        <div className="flex flex-col">
          <span className="text-xs font-bold uppercase tracking-widest">Logged In</span>
          <span className="text-sm tracking-tighter font-mono">{user.email}</span>
        </div>
        <button 
          onClick={handleSignOut}
          className="px-4 py-2 bg-black text-white text-xs font-bold uppercase tracking-widest hover:bg-gray-800"
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <div className="border border-black p-4 bg-white">
      <h3 className="text-sm font-bold uppercase tracking-widest mb-4">Identity Verification Required</h3>
      <button 
        onClick={handleGoogleSignIn}
        className="w-full px-4 py-3 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 transition-colors"
      >
        Sign in with Google
      </button>
      {error && <p className="text-xs text-red-500 mt-2 uppercase font-bold tracking-widest">{error}</p>}
    </div>
  );
}
