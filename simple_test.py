#!/usr/bin/env python3
"""
CPU Inference Test for LaMa Anime/Manga Inpainting
Model: lama_large_512px.ckpt (trained on anime/manga)
Based on: https://github.com/advimman/lama
"""
import os
import sys
import cv2
import numpy as np
import torch
from PIL import Image
from omegaconf import OmegaConf
import yaml
from saicinpainting.evaluation.utils import move_to_device
from saicinpainting.training.trainers import load_checkpoint

# Configuration
IMAGE_PATH = os.getenv("IMAGE_PATH", "test_input/image1.png")
MASK_PATH = os.getenv("MASK_PATH", "test_input/image1_mask001.png")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "outputs/test_result.png")
MODEL_DIR = os.getenv("MODEL_DIR", "local-model")
CHECKPOINT = os.getenv("MODEL_CKPT", "best_genpref.ckpt")
DEVICE = os.getenv("DEVICE", "cpu")

print("=" * 60)
print("🦙 LaMa Anime/Manga Inpainting - CPU Test")
print("=" * 60)
print(f"Device: {DEVICE}")
print(f"Model: {MODEL_DIR}/models/{CHECKPOINT}")
print(f"Input image: {IMAGE_PATH}")
print(f"Input mask: {MASK_PATH}")
print(f"Output: {OUTPUT_PATH}")
print("=" * 60)

train_config_path = f"{MODEL_DIR}/config.yaml"
with open(train_config_path, "r") as f:
    train_config = OmegaConf.create(yaml.safe_load(f))

train_config.training_model.predict_only = True
train_config.visualizer.kind = "noop"

checkpoint_path = f"{MODEL_DIR}/models/{CHECKPOINT}"
model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location="cpu")
model.freeze()
model.to(torch.device(DEVICE))

print("✅ Model loaded!")

print("Loading test images...")
# Load image
image_pil = Image.open(IMAGE_PATH).convert("RGB")
mask_pil = Image.open(MASK_PATH).convert("L")

# Resize to multiples of 8
orig_size = image_pil.size
new_w = (orig_size[0] // 8) * 8
new_h = (orig_size[1] // 8) * 8
image_pil = image_pil.resize((new_w, new_h), Image.LANCZOS)
mask_pil = mask_pil.resize((new_w, new_h), Image.NEAREST)

image = np.array(image_pil)
mask = np.array(mask_pil)

print(f"Original size: {orig_size}, Resized to: ({new_w}, {new_h})")
print(f"Image shape: {image.shape}")
print(f"Mask shape: {mask.shape}")

# Prepare batch
image_f = image.astype("float32") / 255.0
mask_f = (mask > 0).astype("float32")

image_t = torch.from_numpy(np.transpose(image_f, (2, 0, 1))).unsqueeze(0)
mask_t = torch.from_numpy(mask_f)[None, None, ...]

batch = {"image": image_t, "mask": mask_t}
batch = move_to_device(batch, torch.device(DEVICE))

print("Running inference...")
with torch.no_grad():
    batch["mask"] = (batch["mask"] > 0) * 1
    out = model(batch)
    res = out["inpainted"][0].permute(1, 2, 0).detach().cpu().numpy()

res = np.clip(res * 255, 0, 255).astype("uint8")
res_bgr = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

# Save result
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
cv2.imwrite(OUTPUT_PATH, res_bgr)

print("=" * 60)
print("✅ Inference completed successfully!")
print("=" * 60)
print(f"Output shape: {res.shape}")
print(f"Output file: {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH) / 1024:.2f} KB")
print("=" * 60)

# Also save as PNG with high quality
output_png = OUTPUT_PATH.replace('.png', '_hq.png')
cv2.imwrite(output_png, res_bgr, [cv2.IMWRITE_PNG_COMPRESSION, 3])
print(f"High quality output: {output_png}")
print("=" * 60)

