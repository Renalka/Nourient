#!/bin/bash

cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
time (
  uvicorn services.extraction.main:app --port 8000 &
  uvicorn services.scoring.main:app --port 8001 &
  uvicorn services.auditor.main:app --port 8002 &
  uvicorn services.orchestrator.main:app --port 8003 &
  uvicorn services.detective.main:app --port 8004 &
  uvicorn services.biocontext.main:app --port 8005 &
  uvicorn services.alternatives.main:app --port 8006 &
  uvicorn services.basket.main:app --port 8007 &
  uvicorn services.nutrition.main:app --port 8008 &
  wait
)
