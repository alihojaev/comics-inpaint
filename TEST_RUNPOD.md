# 🧪 Тестирование RunPod Endpoint

## 📋 Результаты теста

### ❌ Первая попытка - ошибка

**Ошибка**: `The size of tensor a (1098) must match the size of tensor b (1104) at non-singleton dimension 2`

**Причина**: Размеры изображения 720x1098 не кратны 8, модель требует кратность 8.

**Решение**: Обновлён `rp_handler_cpu.py` - теперь автоматически ресайзит изображения к кратным 8 размерам.

### ✅ Исправление

**Изменения в `rp_handler_cpu.py`**:
```python
# Always ensure dimensions are multiples of 8 (required by model)
new_w = (new_w // 8) * 8
new_h = (new_h // 8) * 8

# Resize if dimensions changed
if new_w != orig_size[0] or new_h != orig_size[1]:
    image_pil = Image.fromarray(image).resize((new_w, new_h), Image.LANCZOS)
    mask_pil = Image.fromarray(mask).resize((new_w, new_h), Image.NEAREST)
    image = np.array(image_pil)
    mask = np.array(mask_pil)
```

## 🚀 Следующие шаги для RunPod

### 1. Обновить Docker образ

Поскольку код обновлён на GitHub, RunPod нужно пересобрать образ:

```bash
# В RunPod Console:
# 1. Перейти к вашему Endpoint
# 2. Rebuild the image
# 3. Wait for cold start
```

### 2. Тестирование с обновлённым образом

После обновления образа на RunPod, запустите тест:

```bash
# Установите переменные окружения
export RUNPOD_ENDPOINT="https://api.runpod.ai/v2/uw2zpg2tot9e48/run"
export RUNPOD_API_KEY="ВАШ_API_KEY"

# Запустите тест
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint
python3 test_runpod_endpoint.py
```

### 3. Ожидаемый результат

```
============================================================
🧪 Testing RunPod Endpoint
============================================================
📷 Input image: test_input/image1.png
🎭 Input mask: test_input/image1_mask001.png
   Image size: (720, 1098)
   Mask size: (720, 1098)

📤 Converting images to base64...
   Image base64 length: 140752 chars
   Mask base64 length: 11800 chars

🚀 Sending request to RunPod...
   Endpoint: https://api.runpod.ai/v2/uw2zpg2tot9e48/run
   Payload size: 152588 bytes

📡 Response received in X.XX seconds
   Status code: 200
   Response keys: ['id', 'status']

⏳ Job queued with ID: XXXXX
   Status: IN_QUEUE

🔄 Checking job status...
   Attempt 1/60: IN_PROGRESS
   Attempt 2/60: COMPLETED

✅ Job completed successfully!

📊 Metadata:
   Input size: [720, 1098]
   Output size: [720, 1096]  # Обратите внимание: 1096 кратно 8
   Device: cpu
   Model: lama_large_512px_anime_manga

💾 Result saved: outputs/runpod_result.png
📁 File size: XXX.XX KB

============================================================
🎉 Test completed successfully!
============================================================
```

## 🔧 Альтернативный тест через cURL

```bash
# Создайте JSON файл с base64 данными
cat > test_request.json <<EOF
{
  "input": {
    "image": "$(base64 -i test_input/image1.png)",
    "mask": "$(base64 -i test_input/image1_mask001.png)"
  }
}
EOF

# Отправьте запрос
curl -X POST https://api.runpod.ai/v2/uw2zpg2tot9e48/run \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer ВАШ_API_KEY' \
    -d @test_request.json
```

## 📊 Ожидаемая производительность

| Параметр | Значение |
|----------|----------|
| **Cold Start** | 10-15 сек |
| **Inference** | 30-60 сек |
| **Total Time** | 40-75 сек |
| **Memory** | ~6-8 GB |
| **CPU** | 8 vCPU |

## 🐛 Известные проблемы

### Проблема 1: Размеры не кратны 8
**Статус**: ✅ Исправлено  
**Решение**: Автоматический ресайз в `rp_handler_cpu.py`

### Проблема 2: API Key в коде
**Статус**: ✅ Исправлено  
**Решение**: Используются переменные окружения

### Проблема 3: Out of Memory
**Статус**: ⚠️  Зависит от размера изображения  
**Решение**: Используйте `MAX_SIZE=1024` или меньше

## 📝 Checklist перед продакшеном

- [x] Код загружен на GitHub
- [x] Исправлена проблема с размерами
- [x] API ключи удалены из кода
- [ ] Docker образ обновлён на RunPod
- [ ] Успешный тест с реальными данными
- [ ] Производительность соответствует ожиданиям
- [ ] Документация обновлена

## 🎯 Следующий тест

После обновления образа на RunPod:

```bash
export RUNPOD_ENDPOINT="https://api.runpod.ai/v2/uw2zpg2tot9e48/run"
export RUNPOD_API_KEY="ВАШ_КЛЮЧ"
python3 test_runpod_endpoint.py
```

---

**Обновлено**: 2025-10-07  
**Статус**: Ожидание обновления образа на RunPod  
**GitHub**: ✅ Обновлён  
**RunPod**: ⏳ Требуется пересборка образа
