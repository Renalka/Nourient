import re

with open('src/components/SidebarLayout.tsx', 'r') as f:
    content = f.read()

target = """          <div className="p-6">
            <div className="p-4 bg-brand-light rounded-xl border border-brand/10">
              <h4 className="text-xs font-bold text-brand uppercase tracking-widest mb-1">Pro Plan</h4>
              <p className="text-[10px] text-gray-500 mb-3">Renews on 12 May, 2026</p>
              <button className="w-full py-2 bg-white text-brand text-xs font-bold rounded-lg border border-brand/20 hover:bg-gray-50 transition-colors">Manage Plan</button>
            </div>
          </div>"""

content = content.replace(target, "")

with open('src/components/SidebarLayout.tsx', 'w') as f:
    f.write(content)

