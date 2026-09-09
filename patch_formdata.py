import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

old_formdata = """    const formData = new FormData();
    formData.append('file', file);
    if (scanMode === 'claims' && file2) {
      formData.append('file2', file2);
    }"""

new_formdata = """    const formData = new FormData();
    if (scanMode === 'claims') {
      formData.append('front_file', file);
      if (file2) formData.append('back_file', file2);
    } else {
      formData.append('file', file);
    }"""

content = content.replace(old_formdata, new_formdata)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
