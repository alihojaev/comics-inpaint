#!/usr/bin/env python3
"""
Test local Docker image to verify the fix works
"""
import base64
import json
import os
import subprocess
from PIL import Image

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def test_local_docker():
    """Test the locally built Docker image"""
    
    print("=" * 60)
    print("🧪 Testing Local Docker Image")
    print("=" * 60)
    
    # Test images
    IMAGE_PATH = "test_input/image1.png"
    MASK_PATH = "test_input/image1_mask001.png"
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Image not found: {IMAGE_PATH}")
        return False
    
    if not os.path.exists(MASK_PATH):
        print(f"❌ Mask not found: {MASK_PATH}")
        return False
    
    print(f"📷 Input image: {IMAGE_PATH}")
    print(f"🎭 Input mask: {MASK_PATH}")
    
    # Get image info
    img = Image.open(IMAGE_PATH)
    mask = Image.open(MASK_PATH)
    print(f"   Image size: {img.size}")
    print(f"   Mask size: {mask.size}")
    
    # Convert to base64
    print("\n📤 Converting images to base64...")
    image_b64 = image_to_base64(IMAGE_PATH)
    mask_b64 = image_to_base64(MASK_PATH)
    
    # Create test input
    test_input = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    # Save to file
    with open("test_docker_input.json", "w") as f:
        json.dump(test_input, f)
    
    print(f"   Payload saved to: test_docker_input.json")
    print(f"   Payload size: {os.path.getsize('test_docker_input.json')} bytes")
    
    # Run Docker container
    print("\n🐳 Running Docker container...")
    
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/test_docker_input.json:/tmp/test_input.json",
        "-v", f"{os.getcwd()}/outputs:/app/outputs",
        "-e", "TEST_MODE=1",
        "lama-anime-runpod-cpu:latest",
        "python3", "-c",
        """
import json
import sys
sys.path.insert(0, '/app')
from rp_handler_cpu import handler

with open('/tmp/test_input.json', 'r') as f:
    event = json.load(f)

result = handler(event)
print(json.dumps(result, indent=2))
"""
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        print(f"\n📡 Docker exit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Success!")
            print("\nOutput:")
            print(result.stdout)
            
            # Try to parse result
            try:
                output = json.loads(result.stdout)
                if output.get("status") == "ok":
                    print("\n🎉 Handler returned OK status!")
                    metadata = output.get("metadata", {})
                    print("\n📊 Metadata:")
                    print(f"   Input size: {metadata.get('input_size')}")
                    print(f"   Output size: {metadata.get('output_size')}")
                    print(f"   Device: {metadata.get('device')}")
                    return True
            except:
                pass
        else:
            print("❌ Failed!")
            print("\nStdout:")
            print(result.stdout)
            print("\nStderr:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Docker container timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    success = test_local_docker()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Local Docker test passed!")
        print("✅ The fix works correctly in Docker")
        print("🚀 Ready to push to Docker Hub for RunPod")
    else:
        print("💥 Local Docker test failed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

