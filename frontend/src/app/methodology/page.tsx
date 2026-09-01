'use client';

import SidebarLayout from '@/components/SidebarLayout';
import AvatarMenu from '@/components/AvatarMenu';
import Breadcrumbs from '@/components/Breadcrumbs';

export default function MethodologyPage() {
  return (
    <SidebarLayout
      pageTitle="Our Methodology"
      pageSubtitle="The foundation of trust and scientifically-backed information."
    >
      <div className="space-y-8 bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        <div>
          <p className="text-gray-600 leading-relaxed text-lg">
            At Nourient, we believe that transparency is the foundation of trust. When you scan a product, our goal is to provide you with the most accurate, scientifically-backed information possible so you can make informed decisions about your health.
          </p>
        </div>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
                <svg className="w-6 h-6 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                Data Sources
              </h2>
              <p className="text-gray-600 leading-relaxed">
                Our intelligence engine does not rely on arbitrary opinions. Instead, it is powered by vast, open-source scientific databases and global food taxonomy repositories, including data modeled after frameworks from international bodies like the European Food Safety Authority (EFSA). By cross-referencing thousands of chemical aliases, we ensure that the information you see is grounded in verified food science.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
                <svg className="w-6 h-6 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                How We Assess Risk
              </h2>
              <p className="text-gray-600 leading-relaxed">
                When evaluating chemical additives, we look at documented toxicology reports regarding <strong>Acceptable Daily Intake (ADI)</strong> thresholds.
              </p>
              <ul className="list-disc pl-5 space-y-2 text-gray-600">
                <li><strong className="text-red-700">High / Moderate Risk:</strong> Indicates that international safety evaluations have found a credible risk of populations exceeding safe daily intake levels through normal consumption.</li>
                <li><strong className="text-green-700">Safe:</strong> Indicates that scientific consensus has determined there is no significant risk of overexposure, or no restrictive intake limit was deemed necessary.</li>
                <li><strong className="text-yellow-700">Permitted Additive:</strong> Indicates a legally recognized food additive where specific overexposure toxicity ratings are not currently mapped in our immediate safety datasets.</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
                <svg className="w-6 h-6 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                Ingredient Categorization
              </h2>
              <p className="text-gray-600 leading-relaxed">
                We categorize ingredients based on their manufacturing origin. A <strong>Natural</strong> or <strong>Natural Derived</strong> label means the ingredient was obtained from a biological source via physical extraction or natural fermentation. A <strong>Synthetic / Processed</strong> label means the ingredient was heavily synthesized or altered in a laboratory environment, even if it mimics a natural compound.
              </p>
            </section>

            <div className="mt-8 p-4 bg-gray-50 rounded-xl border border-gray-100 text-sm text-gray-500 leading-relaxed">
              <strong>Disclaimer:</strong> The information provided by this application is strictly for educational and informational purposes. It is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition or dietary restrictions.
            </div>
          </div>
    </SidebarLayout>
  );
}
