# Используем универсальный образ с поддержкой CUDA
FROM --platform=linux/amd64 nvidia/cuda:11.8.0-devel-ubuntu20.04 as base

# Установка Python и системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \n    python3.11-dev \n    python3-pip \n    gcc \n    g++ \n    && rm -rf /var/lib/apt/lists/* \n    \n    && ln -sf python3.11 /usr/bin/python \n    && ln -sf python3.11 /usr/bin/python3 \n    \n    && pip3 install --upgrade pip \n    \n    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Установка системных зависимостей
# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    \
    # Очистка кэша для уменьшения размера образа
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Установка Python зависимостей с оптимизациями
# Копирование requirements.txt
COPY requirements.txt .

# Установка Python зависимостей с поддержкой CUDA
# Используем специальные сборки PyTorch с CUDA
# Установка PyTorch с автоматическим определением CUDA
RUN pip install \
    --no-cache-dir \
    --timeout 100 \
    --retries 5 \
    --default-timeout=100 \
    torch==2.0.1+cu118 \
    torchvision==0.15.2+cu118 \
    torchaudio==2.0.2+cu118 \
    --extra-index-url https://download.pytorch.org/whl/cu118

# Установка остальных зависимостей
RUN pip install \
    --no-cache-dir \
    --timeout 100 \
    --retries 5 \
    --default-timeout=100 \
    -r requirements.txt

# Копирование приложения
COPY app/ /app/app/

# Копирование конфигурации
COPY config.yaml /app/config.yaml

# Создание директории для векторного хранилища
RUN mkdir -p /app/chroma.db

# Экспорт порта
EXPOSE 80

# Запуск приложения
CMD ["python", "main.py"]