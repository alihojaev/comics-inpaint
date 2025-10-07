#!/usr/bin/env python3
"""
Test script for RunPod Serverless API
"""
import base64
import json
import os
import requests
from PIL import Image
import io

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def base64_to_image(base64_str, output_path):
    """Convert base64 string to image file"""
    img_data = base64.b64decode(base64_str)
    with open(output_path, "wb") as f:
        f.write(img_data)

def test_runpod_api(endpoint_url, api_key, image_path, mask_path):
    """Test RunPod API with local images"""
    
    print("=" * 60)
    print("🧪 Testing RunPod Serverless API")
    print("=" * 60)
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    if not os.path.exists(mask_path):
        print(f"❌ Mask not found: {mask_path}")
        return False
    
    print(f"📷 Input image: {image_path}")
    print(f"🎭 Input mask: {mask_path}")
    
    # Convert images to base64
    print("📤 Converting images to base64...")
    image_b64 = image_to_base64(image_path)
    mask_b64 = image_to_base64(mask_path)
    
    print(f"   Image size: {len(image_b64)} chars")
    print(f"   Mask size: {len(mask_b64)} chars")
    
    # Prepare request
    payload = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Sending request to RunPod...")
    print(f"   Endpoint: {endpoint_url}")
    
    try:
        response = requests.post(
            endpoint_url, 
            json=payload, 
            headers=headers,
            timeout=120  # 2 minutes timeout
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "ok":
                print("✅ Success!")
                
                # Save result
                output_path = "outputs/runpod_result.png"
                os.makedirs("outputs", exist_ok=True)
                base64_to_image(result["image_base64"], output_path)
                
                # Show metadata
                metadata = result.get("metadata", {})
                print("📊 Metadata:")
                print(f"   Input size: {metadata.get('input_size')}")
                print(f"   Output size: {metadata.get('output_size')}")
                print(f"   Device: {metadata.get('device')}")
                print(f"   Model: {metadata.get('model')}")
                
                print(f"💾 Result saved: {output_path}")
                print(f"📁 File size: {os.path.getsize(output_path) / 1024:.2f} KB")
                
                return True
            else:
                print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timeout - try increasing timeout or reducing image size")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main test function"""
    
    # Configuration
    ENDPOINT_URL = os.getenv("RUNPOD_ENDPOINT", "YOUR_ENDPOINT_URL_HERE")
    API_KEY = os.getenv("RUNPOD_API_KEY", "YOUR_API_KEY_HERE")
    
    # Test images
    IMAGE_PATH = os.getenv("TEST_IMAGE", "/Users/alizhan_nh/Desktop/ai/resource-39.jpeg")
    MASK_PATH = os.getenv("TEST_MASK", "/Users/alizhan_nh/Desktop/ai/run-1759581276927-mask.png")
    
    # Check configuration
    if ENDPOINT_URL == "YOUR_ENDPOINT_URL_HERE" or API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please set environment variables:")
        print("   export RUNPOD_ENDPOINT='https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync'")
        print("   export RUNPOD_API_KEY='your_api_key_here'")
        print()
        print("Or edit the script and set ENDPOINT_URL and API_KEY directly")
        return
    
    # Run test
    success = test_runpod_api(ENDPOINT_URL, API_KEY, IMAGE_PATH, MASK_PATH)
    
    if success:
        print("=" * 60)
        print("🎉 Test completed successfully!")
        print("=" * 60)
    else:
        print("=" * 60)
        print("💥 Test failed!")
        print("=" * 60)

if __name__ == "__main__":
    main()
