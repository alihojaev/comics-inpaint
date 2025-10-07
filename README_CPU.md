# 🦙 LaMa Anime/Manga Inpainting - CPU Version

CPU-оптимизированная версия для локального тестирования на основе [advimman/lama](https://github.com/advimman/lama)

## 🎯 Особенности

- ✅ **Специализированная модель**: `lama_large_512px.ckpt` обучена на аниме и манге
- ✅ **CPU оптимизация**: работает на любом компьютере без GPU
- ✅ **Docker**: изолированная среда, легко развернуть
- ✅ **Локальное тестирование**: перед деплоем на RunPod Serverless

## 📦 Структура проекта

```
manga-inpaint/
├── lama_large_512px.ckpt          # Модель (195MB) - обучена на аниме/манге
├── local-model/
│   ├── config.yaml                # Конфигурация модели
│   └── models/
│       └── best_genpref.ckpt      # Копия модели для загрузки
├── test_input/                    # Тестовые изображения
│   ├── image1.png
│   └── image1_mask001.png
├── outputs/                       # Результаты инпейнтинга
├── Dockerfile.cpu                 # CPU версия Dockerfile
├── simple_test.py                 # Тестовый скрипт
└── build_and_test_cpu.sh          # Автоматическая сборка и тест
```

## 🚀 Быстрый старт

### 1. Сборка и тестирование одной командой

```bash
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint
./build_and_test_cpu.sh
```

Этот скрипт:
- ✅ Проверит наличие модели `lama_large_512px.ckpt`
- ✅ Соберёт Docker образ с CPU версией PyTorch
- ✅ Запустит тест на тестовых изображениях
- ✅ Сохранит результаты в `outputs/`

### 2. Ручная сборка

```bash
# Собрать образ
docker build -f Dockerfile.cpu -t lama-anime-cpu:latest .

# Запустить тест
docker run --rm \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    lama-anime-cpu:latest
```

### 3. Обработка своих изображений

```bash
# Положите свои файлы в папку my_images/:
# my_images/image.png - исходное изображение
# my_images/mask.png  - маска (белый = область для инпейнтинга)

docker run --rm \
    -v $(pwd)/my_images:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    -e IMAGE_PATH=/app/test_input/image.png \
    -e MASK_PATH=/app/test_input/mask.png \
    -e OUTPUT_PATH=/app/outputs/result.png \
    lama-anime-cpu:latest
```

## 📊 Технические детали

### Модель
- **Название**: `lama_large_512px.ckpt`
- **Размер**: 195 MB
- **Обучение**: специально на датасете аниме/манги
- **Источник**: [HuggingFace - AnimeMangaInpainting](https://huggingface.co/dreMaz/AnimeMangaInpainting)
- **Архитектура**: FFC-ResNet (Fourier Feature Convolution)
- **Базовый репозиторий**: [advimman/lama](https://github.com/advimman/lama)

### Зависимости
- Python 3.10
- PyTorch 2.4.1 (CPU)
- albumentations==0.5.2 (важно! не новее)
- OpenCV, NumPy, PIL

### Требования к изображениям
- Размеры должны быть кратны 8 пикселям (автоматически ресайзятся)
- Поддерживаемые форматы: PNG, JPEG
- Маска: черный фон, белые области для инпейнтинга

## 🔧 Переменные окружения

```bash
DEVICE=cpu                              # Устройство (cpu/cuda)
MODEL_DIR=local-model                   # Путь к папке с моделью
MODEL_CKPT=best_genpref.ckpt           # Название чекпоинта
IMAGE_PATH=test_input/image1.png       # Исходное изображение
MASK_PATH=test_input/image1_mask001.png # Маска
OUTPUT_PATH=outputs/test_result.png    # Выходной файл
```

## 📝 Примеры использования

### Базовый тест
```bash
docker run --rm \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    lama-anime-cpu:latest
```

### Обработка конкретных файлов
```bash
docker run --rm \
    -v $(pwd)/my_images:/app/input \
    -v $(pwd)/results:/app/output \
    -e IMAGE_PATH=/app/input/anime.png \
    -e MASK_PATH=/app/input/mask.png \
    -e OUTPUT_PATH=/app/output/result.png \
    lama-anime-cpu:latest
```

### Интерактивный режим (для отладки)
```bash
docker run --rm -it \
    -v $(pwd)/test_input:/app/test_input \
    -v $(pwd)/outputs:/app/outputs \
    --entrypoint /bin/bash \
    lama-anime-cpu:latest

# Внутри контейнера:
python3 simple_test.py
```

## 🎯 Следующие шаги

После успешного локального тестирования:

1. ✅ **Проверить качество** результатов в `outputs/`
2. 🔄 **Настроить модель** (если нужно)
3. 🚀 **Задеплоить на RunPod Serverless** (CPU версия)

## 🐛 Решение проблем

### Ошибка: "albumentations DualIAATransform not found"
```bash
# Используйте точно версию 0.5.2
pip install albumentations==0.5.2
```

### Ошибка: "RuntimeError: The size of tensor a must match b"
```bash
# Размеры изображения должны быть кратны 8
# Скрипт автоматически ресайзит, проверьте входные данные
```

### Образ слишком долго собирается
```bash
# Первая сборка занимает 5-10 минут (загрузка PyTorch)
# Последующие сборки используют кэш и проходят быстро
```

## 📚 Ссылки

- [LaMa Official Repository](https://github.com/advimman/lama)
- [LaMa Project Page](https://advimman.github.io/lama-project/)
- [AnimeMangaInpainting Model](https://huggingface.co/dreMaz/AnimeMangaInpainting)
- [Paper: Resolution-robust Large Mask Inpainting with Fourier Convolutions](https://arxiv.org/abs/2109.07161)

## 📄 Лицензия

Apache-2.0 (как в оригинальном LaMa)

