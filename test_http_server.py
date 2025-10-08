#!/usr/bin/env python3
"""
HTTP server for testing the handler locally
"""
import json
import base64
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Add the app directory to Python path
sys.path.insert(0, '/app')

def test_handler():
    print("🧪 Testing handler function...")
    
    # Import the handler function
    from rp_handler_cpu import handler
    
    # Create test payload
    with open("test_input/image1.png", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    
    with open("test_input/image1_mask001.png", "rb") as f:
        mask_b64 = base64.b64encode(f.read()).decode()
    
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
            with open("/app/outputs/http_test_result.png", "wb") as f:
                f.write(base64.b64decode(result["image_base64"]))
            print("💾 Saved result to /app/outputs/http_test_result.png")
        return True
    else:
        print(f"❌ Error: {result.get('message')}")
        return False

if __name__ == "__main__":
    test_handler()
