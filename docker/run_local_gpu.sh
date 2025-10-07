#!/usr/bin/env bash

set -euo pipefail

if (( $# < 3 ))
then
    echo "Usage: $0 model_dir input_dir output_dir [other predict.py args]"
    exit 1
fi

CURDIR="$(dirname "$0")"
SRCDIR="$CURDIR/.."
SRCDIR="$(realpath "$SRCDIR")"

MODEL_LOCAL_DIR="$(realpath "$1")"
INPUT_LOCAL_DIR="$(realpath "$2")"
OUTPUT_LOCAL_DIR="$(realpath "$3")"
shift 3

mkdir -p "$OUTPUT_LOCAL_DIR"
mkdir -p "$INPUT_LOCAL_DIR"

# Build GPU image
docker build -t lama-gpu -f "$SRCDIR/docker/Dockerfile.gpu" "$SRCDIR"

# Run with NVIDIA runtime
docker run --rm \
  --gpus all \
  -v "$SRCDIR":/app \
  -v "$MODEL_LOCAL_DIR":/data/checkpoint \
  -v "$INPUT_LOCAL_DIR":/data/input \
  -v "$OUTPUT_LOCAL_DIR":/data/output \
  lama-gpu \
  model.path=/data/checkpoint \
  indir=/data/input \
  outdir=/data/output \
  ++model.checkpoint=best_genpref.ckpt \
  device=cuda \
  "$@"


