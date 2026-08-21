import Link from 'next/link';

export default function DashboardPage() {
  const features = [
    {
      title: 'Vision Scanner & Score',
      description: 'Upload food labels to instantly extract nutrition facts and generate a multi-dimensional health score.',
      link: '/scanner',
      status: 'ACTIVE'
    },
    {
      title: 'TrueLabel Auditor',
      description: 'Cross-reference marketing claims against actual ingredients using adversarial AI.',
      link: '#',
      status: 'COMING SOON'
    },
    {
      title: 'Better Alternatives',
      description: 'Discover healthier, less-processed alternatives to your favorite snacks.',
      link: '#',
      status: 'COMING SOON'
    },
    {
      title: 'BioContext Profile',
      description: 'Sync your metabolic goals and dietary restrictions for personalized scoring.',
      link: '#',
      status: 'COMING SOON'
    }
  ];

  return (
    <main className="min-h-screen bg-white text-black font-sans selection:bg-black selection:text-white">
      {/* Navigation */}
      <nav className="border-b border-black p-6 flex justify-between items-center max-w-5xl mx-auto">
        <div className="text-xl font-bold tracking-tighter uppercase">Nourient</div>
        <div className="text-xs font-bold uppercase tracking-widest text-gray-500">Guest User</div>
      </nav>

      {/* Main Content */}
      <div className="p-6 md:p-12 max-w-5xl mx-auto space-y-12">
        <header>
          <h1 className="text-3xl font-bold tracking-tighter uppercase mb-2">Dashboard</h1>
          <p className="text-sm text-gray-500 uppercase tracking-widest">Select an intelligence module</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, idx) => (
            <Link 
              key={idx} 
              href={feature.link}
              className={`block p-8 border border-black transition-colors ${feature.status === 'ACTIVE' ? 'hover:bg-gray-50 group cursor-pointer' : 'opacity-50 cursor-not-allowed bg-gray-50'}`}
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-lg font-bold tracking-tighter uppercase">{feature.title}</h2>
                <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 border ${feature.status === 'ACTIVE' ? 'border-black bg-black text-white' : 'border-gray-400 text-gray-400'}`}>
                  {feature.status}
                </span>
              </div>
              <p className="text-sm text-gray-600 leading-relaxed font-medium">
                {feature.description}
              </p>
              
              {feature.status === 'ACTIVE' && (
                <div className="mt-8 text-xs font-bold uppercase tracking-widest text-black group-hover:underline underline-offset-4">
                  Launch Module &rarr;
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
