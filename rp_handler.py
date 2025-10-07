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
DEVICE = os.environ.get("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")


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


def load_model():
    train_config_path = os.path.join(MODEL_DIR, "config.yaml")
    with open(train_config_path, "r") as f:
        train_config = OmegaConf.create(yaml.safe_load(f))
    # predict-only tweaks
    train_config.training_model.predict_only = True
    train_config.visualizer.kind = "noop"

    checkpoint_path = os.path.join(MODEL_DIR, "models", CHECKPOINT)
    model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location="cpu")
    model.freeze()
    model.to(torch.device(DEVICE))
    return model


INPAINTER = load_model()


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    inp = event.get("input", {})

    try:
        image = _read_image(inp["image"])  # RGB HxWx3 uint8
        mask = _read_mask(inp["mask"], target_wh=(image.shape[1], image.shape[0]))  # HxW uint8

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

        return {"status": "ok", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "message": str(e)}


runpod.serverless.start({"handler": handler})


