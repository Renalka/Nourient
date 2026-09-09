import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# 1. Change root div from bg-black to bg-[#F9F9F7]
content = content.replace(
    '<div className="bg-black font-sans overflow-x-hidden" ref={revealRef}>',
    '<div className="bg-[#F9F9F7] font-sans overflow-x-hidden" ref={revealRef}>'
)

# 2. Make the Hero section rounded at the bottom and remove the gradient overlay entirely
hero_start = '<main className="w-full bg-black relative overflow-hidden">'
hero_start_new = '<main className="w-full bg-black relative overflow-hidden rounded-b-[2.5rem] md:rounded-b-[4rem] shadow-2xl z-10">'
content = content.replace(hero_start, hero_start_new)

# 3. Remove the gradient div
gradient_div = """        {/* Bottom fade bridge to next section */}
        <div className="absolute bottom-0 left-0 right-0 h-[400px] bg-gradient-to-t from-[#F9F9F7] via-[#F9F9F7]/60 to-[#F9F9F7]/0 pointer-events-none" />"""
content = content.replace(gradient_div, "")

# 4. We should also make sure the header has a dark background since we changed the root, but the header already has `bg-black/80`.
# And we need to add a bit of padding to the marquee or "how it works" so it doesn't clash with the rounded corners.
# Let's check Marquee:
marquee = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-[#F9F9F7] py-5 border-b border-gray-200 overflow-hidden">"""
marquee_new = """      {/* ── MARQUEE TICKER ───────────────────────────────────── */}
      <div className="bg-[#F9F9F7] pt-12 pb-5 border-b border-gray-200 overflow-hidden">"""
content = content.replace(marquee, marquee_new)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
