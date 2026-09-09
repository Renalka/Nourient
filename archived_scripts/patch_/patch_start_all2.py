with open('start_all.sh', 'r') as f:
    content = f.read()

content = content.replace("backend/.env", ".env")

with open('start_all.sh', 'w') as f:
    f.write(content)
