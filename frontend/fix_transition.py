import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# 1. Restore root div to bg-black so the top of the page remains uniformly black
content = content.replace(
    '<div className="bg-[#F9F9F7] font-sans overflow-x-hidden" ref={revealRef}>',
    '<div className="bg-black font-sans overflow-x-hidden" ref={revealRef}>'
)

# 2. Remove the rounded corners from the hero section
content = content.replace(
    '<section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-20 rounded-b-[2rem] md:rounded-b-[4rem] shadow-2xl z-20 border-b border-white/5">',
    '<section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-20">'
)

# 3. Change Marquee to black theme so it extends the hero section seamlessly
marquee_old = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-[#F9F9F7] pt-12 pb-5 border-b border-gray-200 overflow-hidden">
        <div className="marquee-track">
          {tickerItems.map((item, i) => (
            <span key={i} className="flex items-center gap-3 pr-10 text-[11px] font-bold uppercase tracking-[0.18em] text-gray-400">
              <span className="w-1 h-1 rounded-full bg-gray-300 flex-shrink-0" />"""

marquee_new = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-black py-8 overflow-hidden z-20 relative">
        <div className="marquee-track">
          {tickerItems.map((item, i) => (
            <span key={i} className="flex items-center gap-3 pr-10 text-[11px] font-bold uppercase tracking-[0.18em] text-gray-500">
              <span className="w-1 h-1 rounded-full bg-gray-700 flex-shrink-0" />"""
content = content.replace(marquee_old, marquee_new)

# 4. Insert the SVG Wave Transition right after the marquee
wave_transition = """
      {/* ── SEAMLESS WAVE TRANSITION ─────────────────────────── */}
      <div className="w-full overflow-hidden leading-none bg-[#F9F9F7] relative z-10 -mt-[1px]">
        <svg className="relative block w-full h-[50px] md:h-[100px]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="#000000"></path>
        </svg>
      </div>
"""

# Find where the rest of the content starts and inject the wave
content_start = """      {/* ── REST OF CONTENT on white/off-white background ─────── */}
      <div className="bg-[#F9F9F7]">"""
content = content.replace(content_start, wave_transition + "\n" + content_start)

# Just to make sure we remove the old gradient if it somehow survived (it shouldn't be there based on my last edit, but just in case)
content = re.sub(r'<div className="absolute bottom-0 left-0 right-0 h-\[\d+px\] bg-gradient-to-t.*?>\s*', '', content)
content = re.sub(r'<div className="absolute bottom-0 left-0 right-0 h-\d+ bg-gradient-to-t.*?>\s*', '', content)


with open('src/app/page.tsx', 'w') as f:
    f.write(content)

