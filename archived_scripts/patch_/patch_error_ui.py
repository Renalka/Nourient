with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_err = 'className="mb-6 p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl text-sm font-medium"'
new_err = 'className="mb-6 p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl text-sm font-medium text-center"'

content = content.replace(old_err, new_err)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)

print("Fixed error message alignment")
