#!/usr/bin/env python3
"""
Тест максимального размера изображения для модели
"""
import torch
import sys
import os

# Add app directory to path
sys.path.insert(0, '/app')

def test_max_size():
    try:
        from rp_handler_cpu import load_model
        model = load_model()
        print('✅ Model loaded successfully')
        
        # Тестируем разные размеры (начиная с меньших)
        test_sizes = [512, 768, 1024, 1280, 1536, 1792, 2048]
        
        for size in test_sizes:
            try:
                print(f'\n--- Тестируем размер {size}x{size} ---')
                dummy_image = torch.randn(1, 3, size, size)
                dummy_mask = torch.ones(1, 1, size, size)
                
                with torch.no_grad():
                    result = model({'image': dummy_image, 'mask': dummy_mask})
                
                print(f'✅ {size}x{size} - успешно')
                
            except Exception as e:
                print(f'❌ {size}x{size} - ошибка: {str(e)[:100]}...')
                break
                
    except Exception as e:
        print(f'❌ Ошибка загрузки модели: {e}')

if __name__ == '__main__':
    test_max_size()
