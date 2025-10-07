# 🚀 Deploy Guide - LaMa Anime/Manga Inpainting

## 📋 Что готово

✅ **CPU Docker образ**: `lama-anime-cpu:latest` (4.77GB)  
✅ **Модель**: `lama_large_512px.ckpt` (обучена на аниме/манге)  
✅ **RunPod конфигурация**: `runpod_cpu.yaml`  
✅ **CPU обработчик**: `rp_handler_cpu.py`  
✅ **Тестовые скрипты**: готовы к использованию  
✅ **Документация**: полная  

## 🎯 Быстрый деплой на RunPod

### 1. Подготовка

```bash
# Клонировать репозиторий (если нужно)
git clone https://github.com/alihojaev/comics-inpaint.git
cd comics-inpaint

# Убедиться, что модель на месте
ls -lh lama_large_512px.ckpt  # должно быть ~195MB
```

### 2. Деплой через RunPod CLI

```bash
# Установить RunPod CLI
pip install runpod

# Войти в аккаунт RunPod
runpod login

# Деплой CPU версии
runpod deploy --template runpod_cpu.yaml
```

### 3. Деплой через веб-интерфейс

1. Зайти на [RunPod Console](https://console.runpod.io/serverless)
2. Нажать "New Endpoint"
3. Выбрать "Custom Template"
4. Использовать настройки из `runpod_cpu.yaml`:
   - **GPU**: Disabled
   - **Container Disk**: 10GB
   - **Idle Timeout**: 30 seconds
   - **Max Workers**: 1

## 🧪 Тестирование

### Локальное тестирование

```bash
# Тест с вашими изображениями
python3 test_custom.py

# Тест через Docker
docker run --rm --memory="6g" \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    lama-anime-cpu:latest
```

### Тест RunPod API

```bash
# Установить переменные
export RUNPOD_ENDPOINT="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
export RUNPOD_API_KEY="your_api_key_here"

# Запустить тест
python3 test_runpod_api.py
```

## 📡 API Использование

### Формат запроса

```json
{
  "input": {
    "image": "data:image/jpeg;base64,/9j/4AAQ...",
    "mask": "data:image/png;base64,iVBORw0KGgo..."
  }
}
```

### Формат ответа

```json
{
  "status": "ok",
  "image_base64": "/9j/4AAQ...",
  "metadata": {
    "input_size": [720, 1098],
    "output_size": [512, 328],
    "device": "cpu",
    "model": "lama_large_512px_anime_manga"
  }
}
```

## ⚙️ Настройки

### Переменные окружения

| Переменная | Значение | Описание |
|------------|----------|----------|
| `MODEL_DIR` | `/app/local-model` | Путь к модели |
| `MODEL_CKPT` | `best_genpref.ckpt` | Имя чекпоинта |
| `DEVICE` | `cpu` | Устройство |
| `MAX_SIZE` | `1024` | Макс. размер изображения |

### Оптимизация

```yaml
# Для быстрой обработки
MAX_SIZE: "512"

# Для качественной обработки  
MAX_SIZE: "1024"

# Для очень больших изображений
MAX_SIZE: "1536"
```

## 📊 Производительность

| Размер | Время обработки | Память |
|--------|-----------------|--------|
| 512x512 | ~15-30 сек | ~4GB |
| 1024x1024 | ~30-60 сек | ~6GB |
| 1536x1536 | ~60-120 сек | ~8GB |

## 💰 Стоимость RunPod

- **Cold start**: ~$0.01-0.02 за запрос
- **Warm inference**: ~$0.005-0.01 за запрос
- **Холодный старт**: ~10-15 сек
- **Теплый инференс**: ~10-20 сек

## 🐛 Решение проблем

### Ошибка: "Out of memory"
```yaml
# Уменьшите MAX_SIZE
MAX_SIZE: "512"
```

### Ошибка: "Model not found"
```bash
# Проверьте модель
ls -lh local-model/models/best_genpref.ckpt
```

### Ошибка: "Timeout"
- Увеличьте timeout в RunPod
- Уменьшите размер изображения

## 📚 Полезные ссылки

- **Репозиторий**: https://github.com/alihojaev/comics-inpaint
- **RunPod Console**: https://console.runpod.io
- **LaMa Original**: https://github.com/advimman/lama
- **Модель**: https://huggingface.co/dreMaz/AnimeMangaInpainting

## ✅ Checklist для деплоя

- [ ] Репозиторий загружен на GitHub
- [ ] Модель `lama_large_512px.ckpt` на месте
- [ ] Локальный тест пройден успешно
- [ ] RunPod аккаунт создан
- [ ] Endpoint развернут
- [ ] API тест пройден
- [ ] Документация готова

## 🎉 Готово!

После успешного деплоя у вас будет:
- ✅ Масштабируемый API для инпейнтинга манги/аниме
- ✅ CPU-оптимизированное решение
- ✅ Автоматическое масштабирование
- ✅ Экономичное решение для нечастых запросов

---

**Создано**: 2025-10-07  
**Версия**: CPU Serverless  
**Статус**: Ready for Production 🚀
