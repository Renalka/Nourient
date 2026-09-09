# Nourient

Nourient is an AI-powered nutritional intelligence platform. It analyzes food packaging, audits health claims, flags hidden ingredients, and generates personalized dietary intelligence.

## System Architecture

Nourient operates on a **microservices architecture** with a Next.js client and a decentralized Python backend.

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **State/Auth**: React Context, Firebase Authentication

### Backend Microservices
Written in Python (FastAPI), running concurrently on distinct ports:
- **Extraction (8000)**: OCR & AI image parsing (Gemini Vision)
- **Scoring (8001)**: EFSA-aligned nutritional scoring algorithms
- **Auditor (8002)**: Front-of-pack greenwashing & claim verification
- **Orchestrator (8003)**: Central routing & task delegation
- **Detective (8004)**: Pinecone Vector search & ingredient deep-dives
- **Biocontext (8005)**: User profiling (e.g., Diabetic, Hypertension)
- **Alternatives (8006)**: Healthier product recommendation engine
- **Basket (8007)**: Cumulative macro/micro tracking over time
- **Nutrition (8008)**: Core nutritional database lookups

### AI & Data Infrastructure
- **LLM**: Google Gemini-3.5-flash (Orchestrator, Extraction, Auditor)
- **Vector DB**: Pinecone (Indexes: `patchamomma-ingredients`, `patchamomma-claims`)

---

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Firebase Project (Client & Admin SDK)
- Google Gemini API Key
- Pinecone API Key

### Running the Platform locally

We use bash scripts to manage the cluster.

1. **Boot the cluster**:
   ```bash
   ./start_all.sh
   ```
   *This automatically kills hanging ports, activates the Python virtual environment, pulls variables from `.env`, and boots all 9 microservices alongside the Next.js frontend in the background.*

2. **Access the application**:
   Open [http://localhost:3000](http://localhost:3000) in your browser.

3. **Shutdown**:
   ```bash
   ./stop_all.sh
   ```
   *Safely terminates the `uvicorn` and `next-server` processes.*

---

## Project Structure

- `/frontend` - Next.js client application
- `/backend` - Python FastAPI microservices & ML scripts
- `/archived_scripts` - Legacy one-off patches, fixes, and automation scripts used during development
- `/logs` - Output logs for each microservice (generated at runtime)
