# 🦙 LaMa Anime/Manga Inpainting - RunPod Serverless CPU

RunPod Serverless CPU версия для инпейнтинга манги и аниме на основе [LaMa](https://github.com/advimman/lama)

## 🎯 Особенности

- ✅ **Специализированная модель**: `lama_large_512px.ckpt` обучена на аниме/манге
- ✅ **CPU оптимизация**: работает без GPU, экономично
- ✅ **RunPod Serverless**: масштабируемое решение
- ✅ **Автоматический ресайз**: до 1024px для оптимизации памяти
- ✅ **Base64 I/O**: удобная интеграция с API

## 📦 Структура для RunPod

```
manga-inpaint/
├── rp_handler_cpu.py           # CPU обработчик для RunPod
├── runpod_cpu.yaml            # Конфигурация RunPod CPU
├── Dockerfile.runpod_cpu      # Docker образ для RunPod
├── local-model/
│   ├── config.yaml           # Конфигурация модели
│   └── models/
│       └── best_genpref.ckpt # Модель (195MB)
└── saicinpainting/           # Код LaMa
```

## 🚀 Деплой на RunPod

### 1. Подготовка

```bash
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint

# Проверить, что модель есть
ls -lh lama_large_512px.ckpt

# Скопировать в local-model если нужно
cp lama_large_512px.ckpt local-model/models/best_genpref.ckpt
```

### 2. Деплой через RunPod CLI

```bash
# Установить RunPod CLI (если не установлен)
pip install runpod

# Войти в аккаунт
runpod login

# Деплой CPU версии
runpod deploy --template runpod_cpu.yaml
```

### 3. Альтернативный деплой через веб-интерфейс

1. Зайти на [RunPod Console](https://console.runpod.io)
2. Создать новый Serverless Endpoint
3. Использовать конфигурацию из `runpod_cpu.yaml`:
   - **GPU**: Disabled (CPU only)
   - **Template**: Custom
   - **Dockerfile**: `Dockerfile.runpod_cpu`

## 📡 API Использование

### Формат запроса

```json
{
  "input": {
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
    "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

### Формат ответа

```json
{
  "status": "ok",
  "image_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "metadata": {
    "input_size": [720, 1098],
    "output_size": [512, 328],
    "device": "cpu",
    "model": "lama_large_512px_anime_manga"
  }
}
```

### Пример с Python

```python
import requests
import base64
from PIL import Image
import io

# Подготовка изображений
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Ваш RunPod endpoint
ENDPOINT_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"

# Запрос
payload = {
    "input": {
        "image": image_to_base64("input.png"),
        "mask": image_to_base64("mask.png")
    }
}

response = requests.post(ENDPOINT_URL, json=payload, headers={
    "Authorization": "Bearer YOUR_API_KEY"
})

result = response.json()

if result["status"] == "ok":
    # Сохранение результата
    img_data = base64.b64decode(result["image_base64"])
    with open("output.png", "wb") as f:
        f.write(img_data)
    print("✅ Inpainting completed!")
else:
    print(f"❌ Error: {result['message']}")
```

## 🔧 Настройки

### Переменные окружения

```yaml
env:
  - key: MODEL_DIR
    value: /app/local-model
  - key: MODEL_CKPT
    value: best_genpref.ckpt
  - key: DEVICE
    value: cpu
  - key: MAX_SIZE
    value: "1024"  # Максимальный размер изображения
  - key: MODEL_URL
    value: "https://huggingface.co/dreMaz/AnimeMangaInpainting/resolve/main/lama_large_512px.ckpt?download=true"
```

### Оптимизация производительности

- **MAX_SIZE**: уменьшите для быстрой обработки (512, 768, 1024)
- **Timeout**: увеличьте для больших изображений (30-60 сек)
- **Memory**: RunPod автоматически выделяет достаточно памяти для CPU

## 📊 Ожидаемая производительность

**CPU (RunPod Serverless)**
- Загрузка модели: ~10-15 сек (cold start)
- Inference 512x512: ~15-30 сек
- Inference 1024x1024: ~30-60 сек
- Warm inference: ~10-20 сек (после загрузки)

## 🐛 Решение проблем

### Ошибка: "Out of memory"
```yaml
# Уменьшите MAX_SIZE в runpod_cpu.yaml
- key: MAX_SIZE
  value: "512"
```

### Ошибка: "Model not found"
```bash
# Проверьте, что модель скопирована
ls -lh local-model/models/best_genpref.ckpt
```

### Ошибка: "Timeout"
- Увеличьте timeout в RunPod конфигурации
- Уменьшите размер входного изображения

## 💰 Стоимость

RunPod Serverless CPU:
- **Cold start**: ~$0.01-0.02 за запрос
- **Warm inference**: ~$0.005-0.01 за запрос
- **Экономично** для нечастых запросов

## 📚 Документация

- [LaMa Original](https://github.com/advimman/lama) - базовый репозиторий
- [RunPod Serverless](https://docs.runpod.io/serverless/) - документация RunPod
- [AnimeMangaInpainting Model](https://huggingface.co/dreMaz/AnimeMangaInpainting) - модель

## 📄 Лицензия

Apache-2.0 (как в оригинальном LaMa)

---

**Версия**: CPU Serverless  
**Модель**: lama_large_512px.ckpt  
**Платформа**: RunPod Serverless  
**Оптимизация**: Аниме/манга
