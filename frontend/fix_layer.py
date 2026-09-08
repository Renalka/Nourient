import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# 1. Remove the wave
wave_pattern = r'\{\/\* ── SEAMLESS WAVE TRANSITION ─────────────────────────── \*\/.*?<\/svg>\n      <\/div>'
content = re.sub(wave_pattern, '', content, flags=re.DOTALL)

# 2. Modify the "REST OF CONTENT" wrapper to be an overlapping rounded sheet
content_start_old = """      {/* ── REST OF CONTENT on white/off-white background ─────── */}
      <div className="bg-[#F9F9F7]">"""

content_start_new = """      {/* ── REST OF CONTENT (Overlapping Sheet) ─────── */}
      <div className="bg-[#F9F9F7] relative z-30 rounded-t-[2.5rem] md:rounded-t-[4rem] shadow-[0_-20px_60px_rgba(0,0,0,0.8)] -mt-6">"""

content = content.replace(content_start_old, content_start_new)

# 3. Add a bit of extra padding to the marquee at the bottom so the overlapping sheet doesn't cut off text
marquee_old = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-black py-8 overflow-hidden z-20 relative">"""
marquee_new = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-black pt-8 pb-16 overflow-hidden z-20 relative">"""
content = content.replace(marquee_old, marquee_new)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
