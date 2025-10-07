#!/usr/bin/env bash

set -euo pipefail

if (( $# < 3 )); then
  echo "Usage: $0 <model_dir> <input_dir> <output_dir> [extra predict.py args]"
  exit 1
fi

MODEL_DIR=$(realpath "$1")
INPUT_DIR=$(realpath "$2")
OUTPUT_DIR=$(realpath "$3")
shift 3

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJ_DIR="$(realpath "$SCRIPT_DIR/..")"

mkdir -p "$OUTPUT_DIR"

IMAGE_NAME="lama-cpu-local:latest"

DOCKER_BUILDKIT=1 docker build --platform=linux/amd64 -f "$SCRIPT_DIR/Dockerfile.cpu.local" -t "$IMAGE_NAME" "$PROJ_DIR"

docker run --rm --platform=linux/amd64 \
  -v "$PROJ_DIR":/app \
  -v "$MODEL_DIR":/data/checkpoint \
  -v "$INPUT_DIR":/data/input \
  -v "$OUTPUT_DIR":/data/output \
  "$IMAGE_NAME" \
  model.path=/data/checkpoint \
  indir=/data/input \
  outdir=/data/output \
  device=cpu \
  ++model.checkpoint=best_wrapped.ckpt \
  "$@"


