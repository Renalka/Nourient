"use client";
import React, { useState } from 'react';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import SidebarLayout from '@/components/SidebarLayout';
import Breadcrumbs from '@/components/Breadcrumbs';
import { sendEmailVerification, sendPasswordResetEmail, signOut } from "firebase/auth";
import { auth } from "@/lib/firebase/firebase";

export default function ProfilePage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  if (loading) {
    return (
      <SidebarLayout>
        <div className="p-8 max-w-2xl mx-auto animate-pulse">Loading Profile...</div>
      </SidebarLayout>
    );
  }

  if (!user) {
    router.push("/auth");
    return null;
  }

  const handleVerifyEmail = async () => {
    try {
      setError("");
      setMsg("");
      await sendEmailVerification(user);
      setMsg("Verification email sent! Please check your inbox.");
    } catch (err: any) {
      console.error(err);
      setError("Failed to send verification email. Please try again later.");
    }
  };

  const handleResetPassword = async () => {
    if (!user.email) return;
    try {
      setError("");
      setMsg("");
      await sendPasswordResetEmail(auth, user.email);
      setMsg("Password reset email sent! Please check your inbox.");
    } catch (err: any) {
      console.error(err);
      setError("Failed to send reset email. Please try again later.");
    }
  };

  const handleSignOut = async () => {
    await signOut(auth);
    router.push("/");
  };

  return (
    <SidebarLayout
      pageTitle="Profile Settings"
      pageSubtitle="Manage your account and security"
    >
      <div className="space-y-8">

        {(msg || error) && (
          <div className={`p-4 rounded-xl border text-sm font-medium ${error ? 'bg-red-50 text-red-600 border-red-100' : 'bg-green-50 text-brand border-brand/20'}`}>
            {error || msg}
          </div>
        )}

        <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-6">
          
          <div className="flex items-center justify-between border-b border-gray-100 pb-6">
            <div>
              <p className="text-sm font-bold text-foreground">Email Address</p>
              <p className="text-sm text-gray-500">{user.email}</p>
            </div>
            {user.emailVerified ? (
              <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">Verified</span>
            ) : (
              <button onClick={handleVerifyEmail} className="px-4 py-2 bg-brand-light text-brand text-xs font-bold rounded-lg hover:bg-brand hover:text-white transition-colors">
                Verify Email
              </button>
            )}
          </div>

          <div className="flex items-center justify-between border-b border-gray-100 pb-6">
            <div>
              <p className="text-sm font-bold text-foreground">Password</p>
              <p className="text-sm text-gray-500">Change your account password securely</p>
            </div>
            <button onClick={handleResetPassword} className="px-4 py-2 border border-gray-200 text-gray-600 text-xs font-bold rounded-lg hover:bg-gray-50 transition-colors">
              Reset Password
            </button>
          </div>

          <div className="flex items-center justify-between pt-2">
            <div>
              <p className="text-sm font-bold text-red-600">Sign Out</p>
              <p className="text-sm text-gray-500">Log out of your current session</p>
            </div>
            <button onClick={handleSignOut} className="px-4 py-2 bg-red-50 text-red-600 text-xs font-bold rounded-lg hover:bg-red-100 transition-colors">
              Sign Out
            </button>
          </div>

        </div>
      </div>
    </SidebarLayout>
  );
}
