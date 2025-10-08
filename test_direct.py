#!/usr/bin/env python3
"""
Direct test of the handler function without RunPod serverless
"""
import json
import base64
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def test_direct():
    print("🧪 Testing handler directly")
    
    # Import the handler function
    from rp_handler_cpu import handler
    
    # Create test payload
    image_b64 = image_to_base64("test_input/image1.png")
    mask_b64 = image_to_base64("test_input/image1_mask001.png")
    
    payload = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    print("📤 Running handler...")
    
    # Call handler directly
    result = handler(payload)
    
    print("📊 Result:")
    print(json.dumps(result, indent=2))
    
    if result.get("status") == "ok":
        print("✅ SUCCESS!")
        metadata = result.get("metadata", {})
        print(f"Input: {metadata.get('input_size')}")
        print(f"Output: {metadata.get('output_size')}")
        
        # Save result
        if "image_base64" in result:
            with open("/app/outputs/direct_test_result.png", "wb") as f:
                f.write(base64.b64decode(result["image_base64"]))
            print("💾 Saved result to /app/outputs/direct_test_result.png")
    else:
        print(f"❌ Error: {result.get('message')}")

if __name__ == "__main__":
    test_direct()
