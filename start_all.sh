#!/bin/bash

# Kill any existing processes on these ports just in case
lsof -ti :8000,8001,8002,8003,8004,8005,8006,8007,3000 | xargs kill -9 2>/dev/null || true

cd backend
source venv/bin/activate

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Starting microservices..."
uvicorn services.extraction.main:app --host 0.0.0.0 --port 8000 > extraction.log 2>&1 &
uvicorn services.scoring.main:app --host 0.0.0.0 --port 8001 > scoring.log 2>&1 &
uvicorn services.auditor.main:app --host 0.0.0.0 --port 8002 > auditor.log 2>&1 &
uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8003 > orchestrator.log 2>&1 &
uvicorn services.detective.main:app --host 0.0.0.0 --port 8004 > detective.log 2>&1 &
uvicorn services.biocontext.main:app --host 0.0.0.0 --port 8005 > biocontext.log 2>&1 &
uvicorn services.alternatives.main:app --host 0.0.0.0 --port 8006 > alternatives.log 2>&1 &
uvicorn services.basket.main:app --host 0.0.0.0 --port 8007 > basket.log 2>&1 &

uvicorn services.nutrition.main:app --host 0.0.0.0 --port 8008 > nutrition.log 2>&1 &
cd ../frontend
echo "Starting frontend..."
npm run dev > frontend.log 2>&1 &

echo "All services initiated in the background!"
