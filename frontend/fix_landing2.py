import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# Make sure root div is #F9F9F7
if '<div className="bg-black font-sans overflow-x-hidden" ref={revealRef}>' in content:
    content = content.replace(
        '<div className="bg-black font-sans overflow-x-hidden" ref={revealRef}>',
        '<div className="bg-[#F9F9F7] font-sans overflow-x-hidden" ref={revealRef}>'
    )

# Fix Hero section
target_hero = '<section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-20">'
replacement_hero = '<section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-20 rounded-b-[2rem] md:rounded-b-[4rem] shadow-2xl z-20 border-b border-white/5">'
content = content.replace(target_hero, replacement_hero)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
