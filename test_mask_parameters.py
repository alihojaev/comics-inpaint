#!/usr/bin/env python3
"""
Тест различных параметров обработки маски для улучшения качества inpainting
"""

import requests
import base64
import json
import os
from PIL import Image
import io

def image_to_base64(image_path):
    """Конвертирует изображение в base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def save_base64_image(base64_string, output_path):
    """Сохраняет base64 изображение в файл"""
    img_data = base64.b64decode(base64_string)
    with open(output_path, "wb") as f:
        f.write(img_data)

def test_mask_parameters():
    """Тестирует различные параметры обработки маски"""
    
    # Настройки
    endpoint = os.environ.get("RUNPOD_ENDPOINT", "http://localhost:8080/run")
    api_key = os.environ.get("RUNPOD_API_KEY", "")
    
    image_path = "test_input/image1.png"
    mask_path = "test_input/image1_mask001.png"
    
    if not os.path.exists(image_path) or not os.path.exists(mask_path):
        print("❌ Тестовые файлы не найдены")
        return
    
    image_b64 = image_to_base64(image_path)
    mask_b64 = image_to_base64(mask_path)
    
    # Тестовые конфигурации
    test_configs = [
        {
            "name": "default",
            "params": {}
        },
        {
            "name": "no_blur",
            "params": {"blur_edges": False}
        },
        {
            "name": "light_blur",
            "params": {"blur_edges": True, "blur_radius": 3, "feather_amount": 0.05}
        },
        {
            "name": "medium_blur",
            "params": {"blur_edges": True, "blur_radius": 5, "feather_amount": 0.1}
        },
        {
            "name": "heavy_blur",
            "params": {"blur_edges": True, "blur_radius": 8, "feather_amount": 0.2}
        },
        {
            "name": "extra_smooth",
            "params": {"blur_edges": True, "blur_radius": 10, "feather_amount": 0.3}
        }
    ]
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    os.makedirs("outputs", exist_ok=True)
    
    print("🧪 Тестирование параметров обработки маски...")
    print("=" * 60)
    
    for config in test_configs:
        print(f"\n📋 Тест: {config['name']}")
        print(f"   Параметры: {config['params']}")
        
        payload = {
            "input": {
                "image": image_b64,
                "mask": mask_b64,
                **config['params']
            }
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("status") == "ok":
                    output_path = f"outputs/mask_test_{config['name']}.png"
                    save_base64_image(result["image_base64"], output_path)
                    
                    metadata = result.get("metadata", {})
                    mask_info = metadata.get("mask_processing", {})
                    
                    print(f"   ✅ Успешно сохранено: {output_path}")
                    print(f"   📊 Обработка маски: {mask_info}")
                else:
                    print(f"   ❌ Ошибка: {result.get('message', 'Неизвестная ошибка')}")
            else:
                print(f"   ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование завершено!")
    print("📁 Проверьте папку 'outputs' для сравнения результатов")

if __name__ == "__main__":
    test_mask_parameters()
