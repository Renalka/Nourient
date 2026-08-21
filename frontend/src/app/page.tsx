import Link from 'next/link';

export default function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col justify-center items-center bg-white text-black font-sans selection:bg-black selection:text-white p-6">
      <div className="w-full max-w-sm space-y-12">
        <header className="text-center space-y-4">
          <h1 className="text-5xl font-bold tracking-tighter uppercase">Nourient</h1>
          <p className="text-xs text-gray-500 uppercase tracking-widest">Personalized Food Intelligence</p>
        </header>

        <div className="space-y-4 pt-8 border-t border-black">
          <button className="w-full px-8 py-3 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-gray-800 transition-colors border border-black">
            Log In
          </button>
          <button className="w-full px-8 py-3 bg-white text-black text-sm font-bold uppercase tracking-widest hover:bg-gray-50 transition-colors border border-black">
            Sign Up
          </button>
          
          <div className="pt-4 text-center">
            <Link 
              href="/dashboard" 
              className="text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black transition-colors underline underline-offset-4"
            >
              Continue as Guest
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
