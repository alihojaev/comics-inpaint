# 🔄 RunPod Update Guide

## ⚠️ Проблема

RunPod endpoint использует **старый образ** Docker, в котором нет исправления для размеров изображений.

### Ошибка:
```
The size of tensor a (1098) must match the size of tensor b (1104) at non-singleton dimension 2
```

### Причина:
- Изображение размером 720x1098 не кратно 8
- Модель требует размеры кратные 8
- Старый код не проверял и не ресайзил изображения

### Решение:
Обновлён `rp_handler_cpu.py` - теперь **всегда** ресайзит к кратным 8.

## 🚀 Варианты обновления

### Вариант 1: Пересборка на RunPod (Рекомендуется)

1. **Зайти в RunPod Console**:
   ```
   https://console.runpod.io/serverless/user/endpoints
   ```

2. **Найти endpoint**: `uw2zpg2tot9e48`

3. **Rebuild Image**:
   - Нажать `Settings` или `Edit`
   - Нажать `Rebuild Image` или `Redeploy`
   - Дождаться завершения (5-10 минут)

4. **Протестировать**:
   ```bash
   export RUNPOD_ENDPOINT="https://api.runpod.ai/v2/uw2zpg2tot9e48/run"
   export RUNPOD_API_KEY="ВАШ_КЛЮЧ"
   python3 test_runpod_endpoint.py
   ```

### Вариант 2: Push в Docker Hub

1. **Login в Docker Hub**:
   ```bash
   docker login
   ```

2. **Tag Image**:
   ```bash
   docker tag lama-anime-runpod-cpu:latest YOUR_USERNAME/lama-anime-runpod-cpu:latest
   docker tag lama-anime-runpod-cpu:latest YOUR_USERNAME/lama-anime-runpod-cpu:v1.0
   ```

3. **Push**:
   ```bash
   docker push YOUR_USERNAME/lama-anime-runpod-cpu:latest
   docker push YOUR_USERNAME/lama-anime-runpod-cpu:v1.0
   ```

4. **Обновить в RunPod**:
   - RunPod Console → Endpoint Settings
   - Image: `YOUR_USERNAME/lama-anime-runpod-cpu:latest`
   - Save & Redeploy

### Вариант 3: GitHub Actions (Автоматический)

Создать `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    paths:
      - 'rp_handler_cpu.py'
      - 'Dockerfile.runpod_cpu'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.runpod_cpu
          push: true
          tags: |
            YOUR_USERNAME/lama-anime-runpod-cpu:latest
            YOUR_USERNAME/lama-anime-runpod-cpu:${{ github.sha }}
```

## 📋 Checklist

### Перед обновлением:
- [x] Код исправлен и загружен на GitHub
- [x] Локальный Docker образ собран
- [x] Исправление протестировано (с custom images)
- [ ] Выбран метод обновления

### После обновления:
- [ ] Образ пересобран на RunPod / загружен в Docker Hub
- [ ] Cold start завершён (10-15 сек)
- [ ] Тест с реальными данными успешен
- [ ] Документация обновлена

## 🧪 Проверка успешности

После обновления запустите тест:

```bash
export RUNPOD_ENDPOINT="https://api.runpod.ai/v2/uw2zpg2tot9e48/run"
export RUNPOD_API_KEY="ВАШ_КЛЮЧ"
cd /Users/alizhan_nh/Desktop/ai/manga-inpaint
python3 test_runpod_endpoint.py
```

### Ожидаемый результат:
```
✅ Job completed successfully!

📊 Metadata:
   Input size: [720, 1098]
   Output size: [720, 1096]  # 1096 кратно 8 ✅
   Device: cpu
   Model: lama_large_512px_anime_manga

💾 Result saved: outputs/runpod_result.png
```

## 🐛 Если проблема повторяется

### 1. Проверить, что образ обновлён:
```bash
# На RunPod должен быть последний commit
# Проверить в RunPod Console → Endpoint → Image Details
```

### 2. Проверить логи RunPod:
```
RunPod Console → Endpoint → Logs
# Искать: "Always ensure dimensions are multiples of 8"
```

### 3. Попробовать Force Rebuild:
```
RunPod Console → Endpoint → Settings → Force Rebuild
```

## 📞 Поддержка

- **GitHub Issues**: https://github.com/alihojaev/comics-inpaint/issues
- **RunPod Docs**: https://docs.runpod.io/serverless/
- **RunPod Discord**: https://discord.gg/runpod

---

**Обновлено**: 2025-10-07  
**Статус**: Ожидание обновления на RunPod  
**Приоритет**: Высокий 🔴  
**Действие**: Пересобрать образ на RunPod
