import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_code = """                                <h3 className="text-sm font-bold text-gray-900 mb-1">
                                  {scanMode === 'claims' ? (activeClaimsTab === 'back' ? "Back of Pack" : "Front of Pack") : "Capture Product Label"}
                                </h3>"""

new_code = """                                <h3 className="text-sm font-bold text-gray-900 mb-1">
                                  {scanMode === 'claims' ? (activeClaimsTab === 'back' ? "Ingredients List" : "Front of Pack") : 
                                   scanMode === 'ingredients' ? "Capture Ingredients List" :
                                   scanMode === 'nutrition' ? "Capture Nutrition Facts" :
                                   scanMode === 'front' ? "Capture Front of Pack" :
                                   "Capture Product Label"}
                                </h3>"""

content = content.replace(old_code, new_code)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
