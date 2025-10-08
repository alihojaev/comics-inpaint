#!/usr/bin/env python3
"""
Quick test for local Docker image
"""
import json
import subprocess
import base64
from PIL import Image

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def test_local():
    print("🧪 Quick local Docker test")
    
    # Create test payload
    image_b64 = image_to_base64("test_input/image1.png")
    mask_b64 = image_to_base64("test_input/image1_mask001.png")
    
    payload = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    with open("quick_test.json", "w") as f:
        json.dump(payload, f)
    
    print("📤 Created test payload")
    
    # Run Docker
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{__import__('os').getcwd()}/quick_test.json:/tmp/input.json",
        "-v", f"{__import__('os').getcwd()}/outputs:/app/outputs",
        "lama-anime-runpod-cpu:latest",
        "python3", "-c",
        """
import json
import sys
sys.path.insert(0, '/app')
from rp_handler_cpu import handler

with open('/tmp/input.json', 'r') as f:
    event = json.load(f)

result = handler(event)
print(json.dumps(result, indent=2))
"""
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print(f"Exit code: {result.returncode}")
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                if output.get("status") == "ok":
                    print("✅ SUCCESS!")
                    metadata = output.get("metadata", {})
                    print(f"Input: {metadata.get('input_size')}")
                    print(f"Output: {metadata.get('output_size')}")
                else:
                    print(f"❌ Error: {output.get('message')}")
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_local()
