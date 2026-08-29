#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PWD
nohup uvicorn services.extraction.main:app --host 0.0.0.0 --port 8000 > extraction.log 2>&1 &
nohup uvicorn services.scoring.main:app --host 0.0.0.0 --port 8001 > scoring.log 2>&1 &
nohup uvicorn services.auditor.main:app --host 0.0.0.0 --port 8002 > auditor.log 2>&1 &
nohup uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8003 > orchestrator.log 2>&1 &
nohup uvicorn services.detective.main:app --host 0.0.0.0 --port 8004 > detective.log 2>&1 &
nohup uvicorn services.biocontext.main:app --host 0.0.0.0 --port 8005 > biocontext.log 2>&1 &
nohup uvicorn services.alternatives.main:app --host 0.0.0.0 --port 8006 > alternatives.log 2>&1 &
nohup uvicorn services.basket.main:app --host 0.0.0.0 --port 8007 > basket.log 2>&1 &
echo "All backend services started."
