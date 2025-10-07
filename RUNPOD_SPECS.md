# 🖥️ RunPod Server Specifications - LaMa Anime/Manga Inpainting

## 📊 Рекомендуемые характеристики сервера

### 💰 Вариант 1: Экономичный (для тестирования)
```
CPU: 4 vCPU
RAM: 8 GB
Storage: 10 GB SSD
GPU: None (CPU only)
Cost: ~$0.10-0.20/hour
```

**Подходит для:**
- Разработка и тестирование
- Небольшие изображения (до 512x512)
- Низкая нагрузка

### 🚀 Вариант 2: Стандартный (рекомендуемый)
```
CPU: 8 vCPU
RAM: 16 GB
Storage: 20 GB SSD
GPU: None (CPU only)
Cost: ~$0.20-0.40/hour
```

**Подходит для:**
- Продакшен использование
- Изображения до 1024x1024
- Средняя нагрузка
- Хорошая производительность

### ⚡ Вариант 3: Производительный
```
CPU: 16 vCPU
RAM: 32 GB
Storage: 30 GB SSD
GPU: None (CPU only)
Cost: ~$0.40-0.80/hour
```

**Подходит для:**
- Высокая нагрузка
- Большие изображения (до 1536x1536)
- Минимальное время отклика
- Коммерческое использование

## 🎯 Детальная конфигурация RunPod

### Serverless Configuration (рекомендуется)

```yaml
# runpod_cpu.yaml
name: manga-inpaint-cpu
gpu: false
accelerator: CPU
image: <SET_AFTER_PUSH>
startCommand: |
  python3 /app/rp_handler_cpu.py
env:
  - key: MODEL_DIR
    value: /app/local-model
  - key: MODEL_CKPT
    value: best_genpref.ckpt
  - key: DEVICE
    value: cpu
  - key: MAX_SIZE
    value: "1024"
  - key: MODEL_URL
    value: "https://huggingface.co/dreMaz/AnimeMangaInpainting/resolve/main/lama_large_512px.ckpt?download=true"

# Дополнительные настройки
containerDiskSizeGb: 20
idleTimeout: 30
maxWorkers: 1
```

### Dedicated Server Configuration (для высокой нагрузки)

```yaml
name: manga-inpaint-dedicated
gpu: false
accelerator: CPU
image: <SET_AFTER_PUSH>
startCommand: |
  python3 /app/rp_handler_cpu.py
env:
  - key: MODEL_DIR
    value: /app/local-model
  - key: MODEL_CKPT
    value: best_genpref.ckpt
  - key: DEVICE
    value: cpu
  - key: MAX_SIZE
    value: "1536"
  - key: WORKERS
    value: "4"

# Dedicated settings
containerDiskSizeGb: 50
idleTimeout: 300  # 5 minutes
maxWorkers: 4
```

## 📈 Производительность по размерам сервера

| Характеристики | 4 vCPU/8GB | 8 vCPU/16GB | 16 vCPU/32GB |
|----------------|------------|-------------|--------------|
| **512x512** | 20-30 сек | 15-25 сек | 10-20 сек |
| **1024x1024** | 45-90 сек | 30-60 сек | 20-40 сек |
| **1536x1536** | 120+ сек | 60-120 сек | 40-80 сек |
| **Cold Start** | 15-20 сек | 10-15 сек | 8-12 сек |
| **Warm Start** | 5-8 сек | 3-5 сек | 2-3 сек |

## 💾 Потребление ресурсов

### Память (RAM)
```
Загрузка модели: ~2-3 GB
Inference 512x512: ~4-6 GB
Inference 1024x1024: ~6-8 GB
Inference 1536x1536: ~8-12 GB
```

### Дисковое пространство
```
Docker образ: ~5 GB
Модель: ~200 MB
Система: ~2-3 GB
Резерв: ~2-5 GB
Итого: ~10-15 GB (минимум)
```

### CPU
```
Модель использует все доступные ядра
Оптимально: 8+ vCPU
Минимум: 4 vCPU
```

## 🔧 Настройки по типу использования

### 🧪 Разработка/Тестирование
```
CPU: 4 vCPU
RAM: 8 GB
Storage: 10 GB
Idle Timeout: 30 сек
Max Workers: 1
Cost: ~$0.10-0.20/hour
```

### 🏢 Коммерческое использование
```
CPU: 8 vCPU
RAM: 16 GB
Storage: 20 GB
Idle Timeout: 60 сек
Max Workers: 2-4
Cost: ~$0.20-0.40/hour
```

### 🚀 Высокая нагрузка
```
CPU: 16 vCPU
RAM: 32 GB
Storage: 30 GB
Idle Timeout: 300 сек
Max Workers: 4-8
Cost: ~$0.40-0.80/hour
```

## 📊 Оптимизация затрат

### Serverless vs Dedicated

| Тип | Плюсы | Минусы | Когда использовать |
|-----|-------|--------|-------------------|
| **Serverless** | Оплата за использование | Cold start | Нечастые запросы |
| **Dedicated** | Быстрый отклик | Постоянная оплата | Высокая нагрузка |

### Рекомендации по экономии

1. **Для тестирования**: Serverless 4 vCPU/8GB
2. **Для продакшена**: Serverless 8 vCPU/16GB
3. **Для высокой нагрузки**: Dedicated 16 vCPU/32GB

## 🎯 Итоговые рекомендации

### 🥉 Минимальная конфигурация
```
CPU: 4 vCPU
RAM: 8 GB
Storage: 10 GB
Type: Serverless
Use case: Тестирование, небольшие изображения
```

### 🥈 Рекомендуемая конфигурация
```
CPU: 8 vCPU
RAM: 16 GB
Storage: 20 GB
Type: Serverless
Use case: Продакшен, средняя нагрузка
```

### 🥇 Производительная конфигурация
```
CPU: 16 vCPU
RAM: 32 GB
Storage: 30 GB
Type: Dedicated
Use case: Высокая нагрузка, большие изображения
```

## 💡 Советы по настройке

### Переменные окружения для оптимизации

```yaml
# Для экономии памяти
MAX_SIZE: "512"
WORKERS: "1"

# Для баланса
MAX_SIZE: "1024"
WORKERS: "2"

# Для производительности
MAX_SIZE: "1536"
WORKERS: "4"
```

### Мониторинг производительности

```bash
# Проверка использования ресурсов
docker stats

# Мониторинг в RunPod Console
# Dashboard → Endpoints → Your Endpoint → Metrics
```

## 📞 Поддержка

Если нужна помощь с настройкой:
- RunPod Documentation: https://docs.runpod.io/
- RunPod Discord: https://discord.gg/runpod
- GitHub Issues: https://github.com/alihojaev/comics-inpaint/issues

---

**Обновлено**: 2025-10-07  
**Версия**: CPU Serverless  
**Статус**: Production Ready 🚀
