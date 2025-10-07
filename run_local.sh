#!/bin/bash
# Run inference locally without Docker (for quick testing)

set -e

echo "=========================================="
echo "🦙 LaMa Local CPU Inference"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import torch" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install torch==2.4.1 torchvision==0.19.1 --index-url https://download.pytorch.org/whl/cpu
    pip install albumentations==0.5.2 imgaug==0.4.0
    pip install opencv-python-headless pyyaml omegaconf tqdm easydict scikit-image scikit-learn
    pip install --no-deps pytorch-lightning==1.2.9 kornia==0.5.0
    echo "✅ Dependencies installed"
fi

# Check model
if [ ! -f "lama_large_512px.ckpt" ]; then
    echo "❌ lama_large_512px.ckpt not found!"
    exit 1
fi

# Prepare model directory
if [ ! -f "local-model/models/best_genpref.ckpt" ]; then
    echo "Setting up model..."
    mkdir -p local-model/models
    cp lama_large_512px.ckpt local-model/models/best_genpref.ckpt
fi

# Run inference
echo ""
echo "Running inference..."
export DEVICE=cpu
python3 simple_test.py

echo ""
echo "✅ Done! Check outputs/ directory"
ls -lh outputs/test_result*.png

deactivate

