import base64
import io
import os
import tempfile
from typing import Any, Dict

import cv2
import numpy as np
import torch
from PIL import Image

import runpod

from omegaconf import OmegaConf
import yaml

from saicinpainting.evaluation.utils import move_to_device
from saicinpainting.training.trainers import load_checkpoint


MODEL_DIR = os.environ.get("MODEL_DIR", "/app/local-model")
CHECKPOINT = os.environ.get("MODEL_CKPT", "best_genpref.ckpt")
MODEL_URL = os.environ.get("MODEL_URL", "")
DEVICE = os.environ.get("DEVICE", "cpu")  # Force CPU for RunPod Serverless


def _read_image(data: str) -> np.ndarray:
    """Read image from base64 or URL/file path into RGB np.uint8."""
    if data.startswith("http://") or data.startswith("https://"):
        import requests

        resp = requests.get(data, timeout=60)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        img = Image.open(buf).convert("RGB")
    elif os.path.exists(data):
        img = Image.open(data).convert("RGB")
    else:
        # assume base64
        if "," in data:
            data = data.split(",", 1)[1]
        buf = io.BytesIO(base64.b64decode(data))
        img = Image.open(buf).convert("RGB")
    return np.array(img)


def _read_mask(data: str, target_wh=None) -> np.ndarray:
    """Read mask as single-channel uint8 0/255; resize to image size if needed."""
    if data.startswith("http://") or data.startswith("https://"):
        import requests

        resp = requests.get(data, timeout=60)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        mask_img = Image.open(buf).convert("L")
    elif os.path.exists(data):
        mask_img = Image.open(data).convert("L")
    else:
        if "," in data:
            data = data.split(",", 1)[1]
        buf = io.BytesIO(base64.b64decode(data))
        mask_img = Image.open(buf).convert("L")

    if target_wh is not None and (mask_img.size != target_wh):
        mask_img = mask_img.resize(target_wh, Image.NEAREST)

    return np.array(mask_img)


def _ensure_checkpoint_exists(target_path: str):
    if os.path.exists(target_path):
        return
    if not MODEL_URL:
        raise FileNotFoundError(f"Checkpoint not found at {target_path} and MODEL_URL is not set")
    # download and convert if needed
    import requests
    r = requests.get(MODEL_URL, timeout=300)
    r.raise_for_status()
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(r.content)

    # try wrap to generator.* if it's a raw LaMa gen_state_dict
    try:
        state = torch.load(tmp_path, map_location="cpu")
        if isinstance(state, dict) and "gen_state_dict" in state:
            gen = state["gen_state_dict"]
            if hasattr(gen, "state_dict"):
                gen = gen.state_dict()
            new_sd = {f"generator.{k}": v for k, v in gen.items()}
            torch.save({"state_dict": new_sd}, target_path)
            os.remove(tmp_path)
        elif isinstance(state, dict) and "state_dict" in state:
            # already in expected format
            os.rename(tmp_path, target_path)
        else:
            # fallback: keep as is
            os.rename(tmp_path, target_path)
    except Exception:
        # if any error during wrap, keep original
        os.rename(tmp_path, target_path)


def load_model():
    train_config_path = os.path.join(MODEL_DIR, "config.yaml")
    with open(train_config_path, "r") as f:
        train_config = OmegaConf.create(yaml.safe_load(f))
    # predict-only tweaks
    train_config.training_model.predict_only = True
    train_config.visualizer.kind = "noop"

    checkpoint_path = os.path.join(MODEL_DIR, "models", CHECKPOINT)
    _ensure_checkpoint_exists(checkpoint_path)
    # If downloaded file is a raw gen_state_dict, wrap now
    try:
        state = torch.load(checkpoint_path, map_location="cpu")
        if isinstance(state, dict) and "gen_state_dict" in state:
            gen = state["gen_state_dict"]
            if hasattr(gen, "state_dict"):
                gen = gen.state_dict()
            new_sd = {f"generator.{k}": v for k, v in gen.items()}
            torch.save({"state_dict": new_sd}, checkpoint_path)
    except Exception:
        pass
    model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location="cpu")
    model.freeze()
    model.to(torch.device(DEVICE))
    return model


# Global model loading - optimized for fast startup
print("[rp_handler_cpu] Loading model...")
INPAINTER = load_model()
print(f"[rp_handler_cpu] Model loaded on {DEVICE}")

# Warm up model with dummy inference to cache computations
print("[rp_handler_cpu] Warming up model...")
try:
    dummy_image = torch.randn(1, 3, 64, 64)
    dummy_mask = torch.ones(1, 1, 64, 64)
    with torch.no_grad():
        _ = INPAINTER({"image": dummy_image, "mask": dummy_mask})
    print("[rp_handler_cpu] Model warmed up and ready!")
except Exception as e:
    print(f"[rp_handler_cpu] Warning: Could not warm up model: {e}")
    print("[rp_handler_cpu] Model loaded but not warmed up")


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    inp = event.get("input", {})

    try:
        image = _read_image(inp["image"])  # RGB HxWx3 uint8
        mask = _read_mask(inp["mask"], target_wh=(image.shape[1], image.shape[0]))  # HxW uint8

        # Auto-resize for memory efficiency and ensure dimensions are multiples of 8
               max_size = int(os.environ.get("MAX_SIZE", "768"))  # Max dimension
        orig_size = (image.shape[1], image.shape[0])
        
        print(f"[INFO] Input size: {orig_size}")
        
        # Calculate new dimensions
        if max(orig_size) > max_size:
            ratio = max_size / max(orig_size)
            new_w = int(orig_size[0] * ratio)
            new_h = int(orig_size[1] * ratio)
        else:
            new_w = orig_size[0]
            new_h = orig_size[1]
        
        # Always ensure dimensions are multiples of 8 (required by model)
        new_w = (new_w // 8) * 8
        new_h = (new_h // 8) * 8
        
        print(f"[INFO] Adjusted size: ({new_w}, {new_h}) - multiples of 8")
        
        # Resize if dimensions changed
        if new_w != orig_size[0] or new_h != orig_size[1]:
            print(f"[INFO] Resizing from {orig_size} to ({new_w}, {new_h})")
            image_pil = Image.fromarray(image).resize((new_w, new_h), Image.LANCZOS)
            mask_pil = Image.fromarray(mask).resize((new_w, new_h), Image.NEAREST)
            image = np.array(image_pil)
            mask = np.array(mask_pil)
        else:
            print(f"[INFO] No resize needed")

        # build batch like in predict.py
        image_f = image.astype("float32") / 255.0
        mask_f = (mask > 0).astype("float32")  # binarize

        image_t = torch.from_numpy(np.transpose(image_f, (2, 0, 1))).unsqueeze(0)
        mask_t = torch.from_numpy(mask_f)[None, None, ...]

        batch = {"image": image_t, "mask": mask_t}
        batch = move_to_device(batch, torch.device(DEVICE))

        with torch.no_grad():
            batch["mask"] = (batch["mask"] > 0) * 1
            out = INPAINTER(batch)
            res = out["inpainted"][0].permute(1, 2, 0).detach().cpu().numpy()

        res = np.clip(res * 255, 0, 255).astype("uint8")
        res_bgr = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

        # save to temp file and return base64
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            cv2.imwrite(tmp.name, res_bgr)
            with open(tmp.name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
        os.unlink(tmp.name)

        return {
            "status": "ok", 
            "image_base64": b64,
            "metadata": {
                "input_size": orig_size,
                "output_size": (res.shape[1], res.shape[0]),
                "device": DEVICE,
                "model": "lama_large_512px_anime_manga"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if os.environ.get("RUNPOD_SERVERLESS") or os.environ.get("RUNPOD_POD_ID"):
    runpod.serverless.start({"handler": handler})
else:
    print("[rp_handler_cpu] Loaded handler in local mode; not starting RunPod worker")
