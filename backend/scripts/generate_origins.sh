#!/bin/bash
source ../.env

if [ -z "$GEMINI_API_KEY" ]; then
    echo "No API Key found"
    exit 1
fi

echo "Extracting E-numbers..."
# Extract E-numbers and format into a JSON array
ENUMBERS=$(cat ../services/detective/data/additives.json | grep -o '"en:e[0-9a-z]*"' | sort | uniq | paste -sd, -)
ENUMBERS="[$ENUMBERS]"

echo "Calling Gemini API..."

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}" \
-H 'Content-Type: application/json' \
-d '{
  "contents": [{
    "parts": [{
      "text": "You are a world-class food chemist and regulatory expert. Categorize the following list of E-numbers (food additives) into one of these strict categories based on their origin and manufacturing process: Natural, Natural Derived, Synthetic / Processed, Unknown. Return ONLY a valid, raw JSON object mapping the exact string to its category. Do NOT wrap it in markdown. List to categorize: '"$ENUMBERS"'"
    }]
  }],
  "generationConfig": {
    "responseMimeType": "application/json"
  }
}' > response.json

cat response.json | grep -o '"text": "[^"]*"' | sed 's/"text": "//g' | sed 's/"$//g' | sed 's/\\n/\n/g' | sed 's/\\"/"/g' > ../services/detective/data/chemical_origins.json

echo "Done! Generated $(wc -l < ../services/detective/data/chemical_origins.json) lines."
