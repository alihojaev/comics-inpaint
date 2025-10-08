#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1

# If running on RunPod Serverless, start the handler; else just run handler once for testing
if [[ "${RUNPOD_SERVERLESS:-}" != "" || "${RUNPOD_POD_ID:-}" != "" ]]; then
  echo "[start.sh] Starting Runpod Serverless handler"
  exec python3 /app/rp_handler_cpu.py
else
  echo "[start.sh] Local testing mode - handler will exit after loading"
  echo "[start.sh] This is normal for local testing without RunPod environment"
  python3 /app/rp_handler_cpu.py || true
  echo "[start.sh] Handler test completed"
fi
