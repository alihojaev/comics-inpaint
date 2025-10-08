#!/usr/bin/env python3
"""
Pre-load model during Docker build to reduce startup time
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, '/app')

print('Pre-loading model during Docker build...')

try:
    from rp_handler_cpu import load_model
    model = load_model()
    print('Model pre-loaded successfully!')
    
    # Warm up with dummy inference
    print('Warming up model...')
    import torch
    dummy_image = torch.randn(1, 3, 64, 64)
    dummy_mask = torch.ones(1, 1, 64, 64)
    with torch.no_grad():
        _ = model({"image": dummy_image, "mask": dummy_mask})
    print('Model warmed up and ready!')
    
except Exception as e:
    print(f'Warning: Could not pre-load model: {e}')
    print('Model will be loaded at runtime')
    sys.exit(1)
