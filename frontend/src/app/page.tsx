import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <img src="/logo.png" alt="Nourient Logo" className="w-6 h-6 object-contain" />
          <span className="font-bold tracking-widest text-sm text-brand uppercase">Nourient</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          <span className="hover:text-brand cursor-pointer">How it works</span>
          <span className="hover:text-brand cursor-pointer">Features</span>
          <span className="hover:text-brand cursor-pointer">For everyone</span>
          <span className="hover:text-brand cursor-pointer">Science</span>
          <span className="hover:text-brand cursor-pointer">Pricing</span>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/auth">
            <span className="text-sm font-medium text-gray-600 hover:text-brand">Log in</span>
          </Link>
          <Link href="/auth">
            <button className="px-5 py-2 bg-brand text-white rounded-lg text-sm font-medium hover:bg-brand-dark transition-colors">
              Get Started
            </button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-8 pt-16 pb-24 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        {/* Left Content */}
        <div className="space-y-8">
          <div className="space-y-2">
            <span className="text-[10px] font-bold text-brand uppercase tracking-widest">Food Intelligence, Remagined</span>
            <h1 className="text-6xl font-serif text-brand leading-tight">
              Understand food.<br/>
              <span className="italic font-light">Choose better.</span>
            </h1>
          </div>
          
          <p className="text-gray-600 text-lg max-w-md leading-relaxed">
            Nourient decodes ingredients, verifies claims, and helps you find smarter alternatives—personalized for you.
          </p>

          <div className="flex items-center gap-4">
            <Link href="/scanner">
              <button className="px-6 py-3 bg-brand text-white rounded-lg font-medium hover:bg-brand-dark transition-colors flex items-center gap-2">
                Scan a Product
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
              </button>
            </Link>
            <Link href="/dashboard">
              <button className="px-6 py-3 bg-white text-brand border border-gray-200 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                Explore Demo
              </button>
            </Link>
          </div>

          <div className="pt-8 flex items-center gap-4">
            <div className="flex -space-x-2">
              <div className="w-8 h-8 rounded-full bg-gray-200 border-2 border-background"></div>
              <div className="w-8 h-8 rounded-full bg-gray-300 border-2 border-background"></div>
              <div className="w-8 h-8 rounded-full bg-gray-400 border-2 border-background"></div>
            </div>
            <div className="text-sm">
              <div className="flex items-center gap-1 text-yellow-500">
                ★★★★★
              </div>
              <span className="text-gray-500 text-xs">4.8/5 from 2,500+ reviews</span>
            </div>
          </div>
        </div>

        {/* Right Content - Visual Placeholder */}
        <div className="relative h-[500px] w-full flex items-center justify-center">
          {/* Split Circle Graphic */}
          <div className="relative w-96 h-96 rounded-full border border-gray-200 flex items-center justify-center bg-white shadow-xl overflow-hidden">
             {/* Fake Split representation */}
             <div className="absolute inset-y-0 left-0 w-1/2 bg-brand-light border-r border-gray-200"></div>
             <img src="/logo.png" alt="Nourient Icon" className="absolute z-10 w-16 h-16 object-contain drop-shadow-md" />
          </div>

          {/* Features List overlay */}
          <div className="absolute -right-12 top-1/2 -translate-y-1/2 space-y-6 bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-gray-100 shadow-lg">
            {[
              { title: "Decode", desc: "Ingredients, nutrition & additives" },
              { title: "Verify", desc: "Claims vs. actual facts" },
              { title: "Compare", desc: "Better alternatives, instantly" },
              { title: "Personalize", desc: "Tailored to you & your goals" },
            ].map((feature, i) => (
              <div key={i} className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-brand-light flex items-center justify-center text-brand flex-shrink-0">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                </div>
                <div>
                  <h4 className="font-bold text-sm text-foreground">{feature.title}</h4>
                  <p className="text-xs text-gray-500">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
