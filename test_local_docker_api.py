#!/usr/bin/env python3
"""
Test local Docker container via HTTP API
"""
import json
import base64
import requests
import time

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def test_local_docker():
    print("🧪 Testing local Docker container...")
    
    # Wait a bit for container to fully start
    print("⏳ Waiting for container to start...")
    time.sleep(10)
    
    # Create test payload
    image_b64 = image_to_base64("test_input/image1.png")
    mask_b64 = image_to_base64("test_input/image1_mask001.png")
    
    payload = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    print("📤 Sending request to local container...")
    
    try:
        # Send request to local container
        response = requests.post(
            "http://localhost:8080/rpc",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('status', 'unknown')}")
            
            if result.get("status") == "ok":
                print("🎉 Inpainting successful!")
                print(f"📊 Metadata: {result.get('metadata', {})}")
                
                # Save result
                if "image_base64" in result:
                    with open("outputs/local_test_result.png", "wb") as f:
                        f.write(base64.b64decode(result["image_base64"]))
                    print("💾 Saved result to outputs/local_test_result.png")
            else:
                print(f"❌ Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_local_docker()
