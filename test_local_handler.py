#!/usr/bin/env python3
"""
Test local handler with image files (simulates RunPod call)
"""
import base64
import os
import sys
from PIL import Image

# Add project to path
sys.path.insert(0, '/Users/alizhan_nh/Desktop/ai/manga-inpaint')

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def base64_to_image(base64_str, output_path):
    """Convert base64 string to image file"""
    img_data = base64.b64decode(base64_str)
    with open(output_path, "wb") as f:
        f.write(img_data)

def test_handler():
    """Test handler locally"""
    
    print("=" * 60)
    print("🧪 Testing Local Handler (RunPod simulation)")
    print("=" * 60)
    
    # Import handler
    from rp_handler_cpu import handler
    
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
    
    # Simulate RunPod event
    event = {
        "input": {
            "image": image_b64,
            "mask": mask_b64
        }
    }
    
    print("\n🚀 Calling handler...")
    result = handler(event)
    
    print("\n📡 Handler response:")
    print(f"   Status: {result.get('status')}")
    
    if result.get("status") == "ok":
        print("✅ Success!")
        
        # Save result
        output_path = "outputs/local_handler_result.png"
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
        print(f"❌ Error: {result.get('message')}")
        return False

def main():
    try:
        success = test_handler()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 Test completed successfully!")
        else:
            print("💥 Test failed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

