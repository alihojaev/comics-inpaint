# 🚀 Быстрый старт - LaMa Anime/Manga CPU

## ✅ Что уже готово

1. **Модель**: `lama_large_512px.ckpt` (195MB) - обучена на аниме/манге
2. **CPU Dockerfile**: `Dockerfile.cpu` - оптимизирован для CPU
3. **Тестовый скрипт**: `simple_test.py` - готов к запуску
4. **Автоматизация**: `build_and_test_cpu.sh` - сборка + тест одной командой

## 🎯 Сейчас идёт

Сборка Docker образа `lama-anime-cpu:latest` (займёт ~5-10 минут первый раз)

Проверить статус:
```bash
tail -f /tmp/docker_build.log
```

Или:
```bash
docker images | grep lama-anime
```

## 🏃 Запуск после сборки

### Вариант 1: Docker (рекомендуется)

```bash
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint

# Базовый тест
docker run --rm \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    lama-anime-cpu:latest

# Результаты в outputs/test_result.png
```

### Вариант 2: Локально (без Docker)

```bash
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint
./run_local.sh
```

Этот скрипт:
- Создаст виртуальное окружение `venv/`
- Установит зависимости
- Запустит inference на CPU
- Результаты в `outputs/`

## 📁 Структура результатов

После запуска в `outputs/` будут:
- `test_result.png` - основной результат
- `test_result_hq.png` - высокое качество

## 🔧 Обработка своих изображений

### Docker
```bash
docker run --rm \
    -v /path/to/your/images:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    -e IMAGE_PATH=/app/test_input/your_image.png \
    -e MASK_PATH=/app/test_input/your_mask.png \
    lama-anime-cpu:latest
```

### Локально
```bash
export IMAGE_PATH=test_input/your_image.png
export MASK_PATH=test_input/your_mask.png
python3 simple_test.py
```

## 📋 Требования к изображениям

- **Формат**: PNG или JPEG
- **Маска**: 
  - Чёрный фон (0, 0, 0)
  - Белые области для инпейнтинга (255, 255, 255)
- **Размеры**: автоматически подгоняются к кратным 8

## 🎨 Пример маски

```
Исходное изображение:    Маска:                Результат:
┌─────────────┐          ┌─────────────┐        ┌─────────────┐
│   ANIME     │          │   ░░░░░     │        │   ANIME     │
│   🧍‍♀️ [X]   │  +       │   ░░░█░░    │   =    │   🧍‍♀️ [✓]  │
│   SCENE     │          │   ░░░░░     │        │   SCENE     │
└─────────────┘          └─────────────┘        └─────────────┘
                         (█ = область)           (восстановлено)
```

## 🐛 Частые проблемы

### Docker образ не собрался
```bash
# Проверить логи
tail -100 /tmp/docker_build.log

# Попробовать снова
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint
docker build -f Dockerfile.cpu -t lama-anime-cpu:latest .
```

### Нет outputs/
```bash
mkdir -p outputs
```

### Ошибка "module not found"
```bash
# Для локального запуска
rm -rf venv
./run_local.sh
```

## 📊 Ожидаемая производительность

**CPU (Apple Silicon M-series)**
- Загрузка модели: ~5-10 сек
- Inference 512x512: ~10-30 сек
- Inference 1024x1024: ~30-90 сек

**CPU (Intel/AMD)**
- Загрузка модели: ~10-20 сек
- Inference 512x512: ~20-60 сек
- Inference 1024x1024: ~60-180 сек

## 🚀 Следующие шаги

1. ✅ Дождаться завершения сборки
2. ✅ Запустить тест
3. ✅ Проверить качество результатов
4. 📝 Настроить rp_handler.py для RunPod Serverless
5. 🚀 Задеплоить на RunPod

## 📞 Полезные команды

```bash
# Статус сборки
tail -f /tmp/docker_build.log

# Список образов
docker images

# Удалить образ
docker rmi lama-anime-cpu:latest

# Интерактивный режим (отладка)
docker run --rm -it \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    --entrypoint /bin/bash \
    lama-anime-cpu:latest
```

## 📚 Документация

- [README_CPU.md](README_CPU.md) - Полная документация
- [simple_test.py](simple_test.py) - Код inference
- [Dockerfile.cpu](Dockerfile.cpu) - Docker конфигурация
- [LaMa Official](https://github.com/advimman/lama) - Оригинальный репозиторий

---

**Создано**: 2025-10-07  
**Модель**: lama_large_512px.ckpt  
**Платформа**: CPU (локальное тестирование)  
**Цель**: Подготовка к деплою на RunPod Serverless

