#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1

# If running on RunPod Serverless, start the handler; else just run handler once for testing
if [[ "${RUNPOD_SERVERLESS:-}" != "" || "${RUNPOD_POD_ID:-}" != "" ]]; then
  echo "[start.sh] Starting Runpod Serverless handler"
  exec python3 /app/rp_handler_cpu.py
else
  echo "[start.sh] Local mode: starting HTTP API on :8080"
  exec python3 /app/local_api.py
fi
