#!/usr/bin/env bash
set -euo pipefail

export PORT="${PORT:-8080}"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

pids=()

cleanup() {
  for pid in "${pids[@]:-}"; do
    kill "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT INT TERM

start_service() {
  "$@" &
  pids+=("$!")
}

# Start the uvicorn services. We no longer stagger them because the thread limit 
# prevents deadlocks, allowing them to boot quickly in parallel.
start_service uvicorn services.extraction.main:app --host 127.0.0.1 --port 8000
start_service uvicorn services.scoring.main:app --host 127.0.0.1 --port 8001
start_service uvicorn services.auditor.main:app --host 127.0.0.1 --port 8002
start_service uvicorn services.orchestrator.main:app --host 127.0.0.1 --port 8003
start_service uvicorn services.detective.main:app --host 127.0.0.1 --port 8004
start_service uvicorn services.biocontext.main:app --host 127.0.0.1 --port 8005
start_service uvicorn services.alternatives.main:app --host 127.0.0.1 --port 8006
start_service uvicorn services.basket.main:app --host 127.0.0.1 --port 8007
start_service uvicorn services.nutrition.main:app --host 127.0.0.1 --port 8008

echo "Waiting for all backend microservices to bind..."
for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008; do
  while ! curl -s http://127.0.0.1:$port >/dev/null; do 
    sleep 1
  done
  echo "Port $port is up."
done

echo "All Python services are ready. Starting Nginx gateway..."
envsubst '${PORT}' < /etc/nginx/templates/nourient.conf.template > /etc/nginx/nginx.conf
nginx -t
start_service nginx -g 'daemon off;'
echo "Started Nginx. Cloud Run is now ready to receive traffic!"

wait -n "${pids[@]}"
