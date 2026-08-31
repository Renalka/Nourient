import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      {/* Global Enforced Top Bar (Matches Internal App Layout) */}
      <header className="border-b border-gray-200 bg-white px-4 md:px-8 py-3 flex justify-between items-center z-40 shadow-sm sticky top-0 w-full shrink-0">
         
         {/* Left Section: Hamburger + Logo */}
         <div className="flex items-center gap-3 md:gap-6 lg:w-1/3">
           <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none">
             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
           </button>
           
           <Link href="/" className="flex items-center gap-2">
             <img src="/icon.png" alt="Nourient Logo" className="w-8 h-8 object-contain" />
             <span className="font-bold tracking-widest text-sm text-brand uppercase hidden md:block">Nourient</span>
           </Link>
         </div>
         
         {/* Center Section: Navigation Links (Desktop) */}
         <div className="hidden lg:flex flex-1 justify-center gap-2">
           {['How it works', 'Features', 'For everyone', 'Science', 'Pricing'].map((item) => (
             <span key={item} className="px-5 py-2 rounded-full text-xs font-bold text-gray-500 hover:bg-gray-50 hover:text-foreground transition-colors cursor-pointer">
               {item}
             </span>
           ))}
         </div>

         {/* Right Section: Auth Buttons */}
         <div className="flex items-center justify-end gap-4 lg:w-1/3">
            <Link href="/auth">
              <span className="text-xs font-bold text-gray-600 hover:text-brand cursor-pointer transition-colors">Log in</span>
            </Link>
            <Link href="/auth">
              <button className="px-5 py-2 bg-brand text-white rounded-full text-xs font-bold hover:bg-brand-dark transition-colors shadow-sm">
                Get Started
              </button>
            </Link>
         </div>
      </header>

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

          {/*<div className="pt-8 flex items-center gap-4">
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
          </div>*/}
        </div>

        {/* Right Content - Hero Image with Concentric Animated UI */}
        <div className="relative h-[600px] w-full flex items-center justify-center lg:justify-end">
          <div className="relative w-full max-w-2xl h-[500px] flex items-center">
            
            {/* Left Half: Half-Masked Food Bowl */}
            <div className="absolute left-0 w-[200px] h-[400px] top-1/2 -translate-y-1/2 overflow-hidden z-10">
               <div className="absolute left-0 w-[400px] h-[400px] rounded-full overflow-hidden">
                  <img src="/landing-food-bowl.png" alt="Healthy Food Bowl" className="w-full h-full object-cover scale-[1.15]" />
               </div>
            </div>

            {/* Right Half: Animated Semi-Circles */}
            <div className="absolute left-[200px] w-[200px] h-[400px] top-1/2 -translate-y-1/2 overflow-hidden z-0">
                <div className="absolute right-0 w-[400px] h-[400px] flex items-center justify-center">
                    <div className="absolute w-[400px] h-[400px] rounded-full border border-gray-200 animate-spin" style={{ animationDuration: '40s' }}></div>
                    <div className="absolute w-[300px] h-[300px] rounded-full border border-green-200/60 animate-spin" style={{ animationDuration: '30s', animationDirection: 'reverse' }}></div>
                    <div className="absolute w-[200px] h-[200px] rounded-full border border-gray-200 animate-spin" style={{ animationDuration: '20s' }}></div>
                    <div className="absolute w-[100px] h-[100px] rounded-full border border-green-200/40 animate-spin" style={{ animationDuration: '10s', animationDirection: 'reverse' }}></div>
                </div>
            </div>

            {/* Center Dark Green Icon */}
            <div className="absolute left-[200px] top-1/2 -translate-x-1/2 -translate-y-1/2 w-[72px] h-[72px] bg-[#1a3622] rounded-full z-20 flex items-center justify-center shadow-xl border-4 border-white">
                <img src="/icon.png" alt="Nourient Icon" className="w-12 h-12 object-contain invert brightness-0" />
            </div>

            {/* Features List with Connecting Lines */}
            <div className="absolute left-[440px] w-[300px] z-30 flex flex-col justify-center space-y-7">
              {[
                { title: "Decode", desc: "Ingredients, nutrition & additives", line: "w-24" },
                { title: "Verify", desc: "Claims vs. actual facts", line: "w-16" },
                { title: "Compare", desc: "Better alternatives, instantly", line: "w-20" },
                { title: "Personalize", desc: "Tailored to you & your goals", line: "w-16" },
                { title: "Decide", desc: "Smarter choices, every day", line: "w-24" },
              ].map((feature, i) => (
                <div key={i} className="relative flex items-center gap-4 group">
                  {/* Dashed line extending into circles */}
                  <div className={`absolute left-0 -translate-x-full ${feature.line} border-b border-gray-200 border-dashed`}></div>
                  {/* Dot on the line */}
                  <div className="absolute left-0 -translate-x-full w-1.5 h-1.5 rounded-full bg-green-600 -translate-y-1/2 top-1/2 opacity-50 group-hover:opacity-100 transition-opacity shadow-sm"></div>
                  
                  <div className="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-gray-500 flex-shrink-0 z-10 shadow-sm border border-gray-100 group-hover:text-brand group-hover:border-brand/30 transition-colors">
                     <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
                  </div>
                  <div>
                    <h4 className="font-bold text-[14px] text-gray-900 leading-tight">{feature.title}</h4>
                    <p className="text-[12px] text-gray-500 mt-0.5 leading-tight">{feature.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Widgets Section */}
      <section className="max-w-7xl mx-auto px-8 pb-32 space-y-8">
        
        {/* Widget 1: Features Card (Clean Black & White) */}
        <div className="bg-white rounded-3xl border border-gray-200 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-10 md:p-12">
          <h3 className="text-center text-xs font-bold tracking-[0.2em] text-gray-900 uppercase mb-12">
            Powerful Features. Built on Science.
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-8 divide-y md:divide-y-0 md:divide-x divide-gray-100">
            
            {/* Feature 1 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 8v-2a2 2 0 012-2h2m10 0h2a2 2 0 012 2v2m-14 10v2a2 2 0 002 2h2m10 0h2a2 2 0 002-2v-2m-3-4l-3-3m0 0l-3 3m3-3v6" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">AI-Powered OCR Scanner</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">Advanced Vision AI extracts every chemical compound with exceptional accuracy.</p>
            </div>

            {/* Feature 2 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">The "Detective" Intelligence Engine</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">Maps aliases to real chemical identities and explains exactly what each ingredient does.</p>
            </div>

            {/* Feature 3 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">Origin Categorization</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">Know the true source of every ingredient: Natural, Natural Derived, or Synthetic.</p>
            </div>

            {/* Feature 4 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">Scientific Risk Assessment</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">EFSA-modeled risk evaluation based on ADI thresholds and toxicology data.</p>
            </div>

            {/* Feature 5 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">Real-Time Ingredient Dictionary</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">Search by name, alias, or E-number with blazing fast autocomplete.</p>
            </div>

            {/* Feature 6 */}
            <div className="flex flex-col items-center text-center px-4 pt-6 md:pt-0">
              <svg className="w-8 h-8 mb-4 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              <h4 className="font-bold text-sm text-gray-900 mb-2">Better Alternatives (Basket)</h4>
              <p className="text-[11px] text-gray-500 leading-relaxed">Compare with healthier whole-food alternatives and build smarter baskets.</p>
            </div>

          </div>
        </div>

        {/* Widget 2: Trust Banner (Dark Monochrome) */}
        <div className="bg-[#111111] rounded-3xl p-8 md:p-10 flex flex-col lg:flex-row items-center justify-between gap-10">
          
          {/* Left Text */}
          <div className="flex items-center gap-6 lg:w-1/3">
            <div className="w-16 h-16 rounded-2xl border border-gray-700 bg-gray-800/50 flex items-center justify-center flex-shrink-0 relative overflow-hidden">
              <div className="absolute inset-0 bg-white/5 opacity-0 hover:opacity-100 transition-opacity"></div>
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
            </div>
            <div>
              <h3 className="text-xl font-serif text-white mb-1">Transparent. Scientific. Trustworthy.</h3>
              <p className="text-sm text-gray-400">Built on global data sources and EFSA toxicology models.</p>
            </div>
          </div>

          {/* Right Metrics Grid */}
          <div className="flex-1 grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-0 md:divide-x divide-gray-800 w-full">
            
            <div className="flex flex-col items-center text-center px-2">
              <svg className="w-6 h-6 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>
              <h4 className="font-bold text-white text-sm mb-1">10,000+</h4>
              <p className="text-[10px] text-gray-500 uppercase tracking-wider">Ingredients Mapped</p>
            </div>

            <div className="flex flex-col items-center text-center px-2">
              <svg className="w-6 h-6 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
              <h4 className="font-bold text-white text-sm mb-1">350+</h4>
              <p className="text-[10px] text-gray-500 uppercase tracking-wider">Scientific References</p>
            </div>

            <div className="flex flex-col items-center text-center px-2">
              <svg className="w-6 h-6 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
              <h4 className="font-bold text-white text-sm mb-1">Global</h4>
              <p className="text-[10px] text-gray-500 uppercase tracking-wider">Data Sources</p>
            </div>

            <div className="flex flex-col items-center text-center px-2">
              <svg className="w-6 h-6 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <h4 className="font-bold text-white text-sm mb-1">Continuous</h4>
              <p className="text-[10px] text-gray-500 uppercase tracking-wider">Model Updates</p>
            </div>

          </div>
        </div>

      </section>
    </div>
  );
}
