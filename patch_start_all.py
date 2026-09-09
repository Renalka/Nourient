with open('start_all.sh', 'r') as f:
    lines = f.readlines()

with open('start_all.sh', 'w') as f:
    for line in lines:
        if "export PINECONE_API_KEY" in line:
            f.write("if [ -f backend/.env ]; then\n  export $(grep -v '^#' backend/.env | xargs)\nfi\n")
        else:
            f.write(line)
