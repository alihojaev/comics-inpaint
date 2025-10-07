# RunPod Serverless build expects Dockerfile in repo root.
# This Dockerfile mirrors docker/Dockerfile.gpu.

FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

COPY docker/requirements_docker.txt /app/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir "numpy<1.22" "scipy<1.8" cython && \
    python3 -m pip install --no-cache-dir -r /app/requirements.txt && \
    python3 -m pip install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118

ARG LAMA_URL="https://huggingface.co/dreMaz/AnimeMangaInpainting/resolve/main/lama_large_512px.ckpt?download=true"
RUN mkdir -p /app/local-model/models && \
    echo "Downloading checkpoint from $LAMA_URL" && \
    curl -L "$LAMA_URL" -o /app/local-model/models/best_genpref.ckpt

COPY . /app

ENTRYPOINT ["python3", "/app/rp_handler.py"]


