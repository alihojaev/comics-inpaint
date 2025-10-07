#!/usr/bin/env python3
"""
Test script for RunPod Endpoint with real image data
"""
import base64
import json
import os
import requests
import time
from PIL import Image

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def base64_to_image(base64_str, output_path):
    """Convert base64 string to image file"""
    img_data = base64.b64decode(base64_str)
    with open(output_path, "wb") as f:
        f.write(img_data)

def test_endpoint():
    """Test RunPod endpoint"""
    
    print("=" * 60)
    print("🧪 Testing RunPod Endpoint")
    print("=" * 60)
    
    # Your endpoint configuration
    ENDPOINT_URL = os.getenv("RUNPOD_ENDPOINT", "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run")
    API_KEY = os.getenv("RUNPOD_API_KEY", "YOUR_API_KEY_HERE")
    
    # Check configuration
    if "YOUR_ENDPOINT_ID" in ENDPOINT_URL or API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please set environment variables:")
        print("   export RUNPOD_ENDPOINT='https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run'")
        print("   export RUNPOD_API_KEY='your_api_key_here'")
        print()
        print("Or run:")
        print("   python3 test_runpod_endpoint.py")
        return False
    
    # Test images
    IMAGE_PATH = "test_input/image1.png"
    MASK_PATH = "test_input/image1_mask001.png"
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Image not found: {IMAGE_PATH}")
        print("Using custom images instead...")
        IMAGE_PATH = "/Users/alizhan_nh/Desktop/ai/resource-39.jpeg"
        MASK_PATH = "/Users/alizhan_nh/Desktop/ai/run-1759581276927-mask.png"
    
    if not os.path.exists(IMAGE_PATH) or not os.path.exists(MASK_PATH):
        print("❌ Test images not found!")
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
    
    print(f"   Image base64 length: {len(image_b64)} chars")
    print(f"   Mask base64 length: {len(mask_b64)} chars")
    
    # Prepare request payload
    payload = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("\n🚀 Sending request to RunPod...")
    print(f"   Endpoint: {ENDPOINT_URL}")
    print(f"   Payload size: {len(json.dumps(payload))} bytes")
    
    try:
        start_time = time.time()
        response = requests.post(
            ENDPOINT_URL,
            json=payload,
            headers=headers,
            timeout=300  # 5 minutes timeout
        )
        elapsed_time = time.time() - start_time
        
        print(f"\n📡 Response received in {elapsed_time:.2f} seconds")
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response keys: {list(result.keys())}")
            
            # Check if it's async response
            if "id" in result:
                print(f"\n⏳ Job queued with ID: {result['id']}")
                print(f"   Status: {result.get('status', 'unknown')}")
                
                # For async endpoints, you need to check status
                status_url = f"https://api.runpod.ai/v2/uw2zpg2tot9e48/status/{result['id']}"
                
                print("\n🔄 Checking job status...")
                max_attempts = 60
                for attempt in range(max_attempts):
                    time.sleep(5)
                    status_response = requests.get(status_url, headers=headers)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        job_status = status_data.get("status", "unknown")
                        print(f"   Attempt {attempt + 1}/{max_attempts}: {job_status}")
                        
                        if job_status == "COMPLETED":
                            output = status_data.get("output", {})
                            if output.get("status") == "ok":
                                print("\n✅ Job completed successfully!")
                                
                                # Save result
                                output_path = "outputs/runpod_result.png"
                                os.makedirs("outputs", exist_ok=True)
                                base64_to_image(output["image_base64"], output_path)
                                
                                metadata = output.get("metadata", {})
                                print("\n📊 Metadata:")
                                print(f"   Input size: {metadata.get('input_size')}")
                                print(f"   Output size: {metadata.get('output_size')}")
                                print(f"   Device: {metadata.get('device')}")
                                print(f"   Model: {metadata.get('model')}")
                                
                                print(f"\n💾 Result saved: {output_path}")
                                print(f"📁 File size: {os.path.getsize(output_path) / 1024:.2f} KB")
                                
                                return True
                            else:
                                print(f"❌ Job failed: {output.get('message', 'Unknown error')}")
                                return False
                        elif job_status == "FAILED":
                            print(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
                            return False
                    else:
                        print(f"   Warning: Status check failed with code {status_response.status_code}")
                
                print("⏰ Timeout waiting for job completion")
                return False
            
            # Direct response (sync endpoint)
            elif result.get("status") == "ok":
                print("✅ Success!")
                
                # Save result
                output_path = "outputs/runpod_result.png"
                os.makedirs("outputs", exist_ok=True)
                base64_to_image(result["image_base64"], output_path)
                
                metadata = result.get("metadata", {})
                print("\n📊 Metadata:")
                print(f"   Input size: {metadata.get('input_size')}")
                print(f"   Output size: {metadata.get('output_size')}")
                print(f"   Device: {metadata.get('device')}")
                print(f"   Model: {metadata.get('model')}")
                
                print(f"\n💾 Result saved: {output_path}")
                print(f"📁 File size: {os.path.getsize(output_path) / 1024:.2f} KB")
                
                return True
            else:
                print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                print(f"   Full response: {json.dumps(result, indent=2)}")
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
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_endpoint()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("💥 Test failed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

