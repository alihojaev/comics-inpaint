#!/bin/bash
# Build and test CPU version of LaMa anime/manga inpainting

set -e

echo "=========================================="
echo "🦙 LaMa Anime/Manga Inpainting - CPU Build"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if lama_large_512px.ckpt exists
if [ ! -f "lama_large_512px.ckpt" ]; then
    echo -e "${YELLOW}⚠️  lama_large_512px.ckpt not found in current directory${NC}"
    echo "This model should be present for anime/manga inpainting"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ Found lama_large_512px.ckpt ($(du -h lama_large_512px.ckpt | cut -f1))${NC}"
fi

# Check if test images exist
if [ ! -f "test_input/image1.png" ] || [ ! -f "test_input/image1_mask001.png" ]; then
    echo -e "${RED}❌ Test images not found in test_input/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Test images found${NC}"

# Build Docker image
echo ""
echo "Building Docker image (CPU version)..."
docker build -f Dockerfile.cpu -t lama-anime-cpu:latest .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

# Run test
echo ""
echo "=========================================="
echo "Running inference test..."
echo "=========================================="

docker run --rm \
    -v "$(pwd)/test_input:/app/test_input" \
    -v "$(pwd)/outputs:/app/outputs" \
    -e DEVICE=cpu \
    lama-anime-cpu:latest

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✅ Test completed successfully!"
    echo "==========================================${NC}"
    echo ""
    echo "Check outputs/ directory for results:"
    ls -lh outputs/test_result*.png 2>/dev/null || echo "No output files found"
else
    echo -e "${RED}❌ Test failed${NC}"
    exit 1
fi

echo ""
echo "To run with your own images:"
echo "  docker run --rm -v \$(pwd)/your_images:/app/test_input -v \$(pwd)/outputs:/app/outputs lama-anime-cpu:latest"

