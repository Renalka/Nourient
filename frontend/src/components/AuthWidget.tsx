"use client";
import React, { useState } from "react";
import { signInWithPopup, GoogleAuthProvider, signOut, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendEmailVerification, sendPasswordResetEmail } from "firebase/auth";
import { auth } from "@/lib/firebase/firebase";
import { useAuth } from "@/context/AuthContext";

export default function AuthWidget() {
  const { user, loading } = useAuth();
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleGoogleSignIn = async () => {
    try {
      setError("");
      setMsg("");
      setIsLoading(true);
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
    } catch (err: any) {
      setError(err.message || "Failed to sign in");
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      setError("Please enter your email address first to reset your password.");
      return;
    }
    try {
      setError("");
      setMsg("");
      setIsLoading(true);
      await sendPasswordResetEmail(auth, email);
      setMsg("If an account exists, a password reset link has been sent to your email.");
    } catch (err: any) {
      // Don't leak whether the email exists or not for security (OWASP)
      setMsg("If an account exists, a password reset link has been sent to your email.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Email and Password are required.");
      return;
    }

    if (!isLoginMode) {
      // OWASP Strong Password Regex: Minimum 8 chars, at least one uppercase, one lowercase, one number, one special character
      const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      if (!strongPasswordRegex.test(password)) {
        setError("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.");
        return;
      }
    }
    
    try {
      setError("");
      setMsg("");
      setIsLoading(true);
      if (isLoginMode) {
        await signInWithEmailAndPassword(auth, email, password);
      } else {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        // Automatically send verification email on successful registration
        await sendEmailVerification(userCredential.user);
      }
    } catch (err: any) {
      let msg = err.message;
      if (msg.includes("auth/invalid-credential") || msg.includes("auth/user-not-found") || msg.includes("auth/wrong-password")) {
        msg = "Invalid email or password.";
      } else if (msg.includes("auth/email-already-in-use")) {
        // We technically shouldn't leak this per OWASP, but for UX it's often standard.
        // To be strictly secure against enumeration: "If this email is not registered, we have sent a link..."
        // But since this is a consumer app, we will use a generic but clear message.
        msg = "An account with this email already exists.";
      }
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignOut = async () => {
    await signOut(auth);
  };

  if (loading) {
    return <div className="text-sm font-medium text-gray-400 text-center py-8">Loading Auth...</div>;
  }

  if (user) {
    return (
      <div className="flex flex-col items-center gap-4 py-4">
        <div className="text-center">
          <p className="text-sm text-gray-500">Signed in as</p>
          <p className="font-medium text-foreground">{user.email}</p>
        </div>
        <button 
          onClick={handleSignOut}
          className="w-full px-6 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors"
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleEmailAuth} className="space-y-4">
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-gray-700">Email address</label>
          <input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-gray-200 rounded-lg p-3 text-sm focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand transition-all"
            placeholder="you@example.com"
            required
          />
        </div>
        
        <div className="space-y-1.5">
          <div className="flex justify-between items-center">
            <label className="text-sm font-medium text-gray-700">Password</label>
            {isLoginMode && (
              <button type="button" onClick={handleForgotPassword} className="text-xs font-medium text-brand hover:underline">
                Forgot password?
              </button>
            )}
          </div>
          <input 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-gray-200 rounded-lg p-3 text-sm focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand transition-all"
            placeholder="••••••••"
            required
            minLength={8}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 text-red-600 rounded-lg text-sm border border-red-100">
            {error}
          </div>
        )}
        
        {msg && (
          <div className="p-3 bg-green-50 text-brand rounded-lg text-sm border border-brand/20">
            {msg}
          </div>
        )}

        <button 
          type="submit"
          disabled={isLoading}
          className="w-full py-3 bg-brand text-white rounded-lg font-medium hover:bg-brand-dark transition-colors disabled:opacity-50"
        >
          {isLoading ? "Authenticating..." : isLoginMode ? "Log In" : "Sign Up"}
        </button>
      </form>

      <div className="text-center pt-2">
        <button 
          type="button"
          onClick={() => {
            setIsLoginMode(!isLoginMode);
            setError("");
            setMsg("");
          }}
          className="text-sm text-brand font-medium hover:underline"
        >
          {isLoginMode ? "Need an account? Sign up" : "Already have an account? Log in"}
        </button>
      </div>
    </div>
  );
}
