#!/bin/bash

cd "$(dirname "$0")/.."

echo "Stopping all microservices and frontend..."
lsof -ti :8000,8001,8002,8003,8004,8005,8006,8007,8008,3000 | xargs kill -9 2>/dev/null || true
echo "All services stopped successfully!"
