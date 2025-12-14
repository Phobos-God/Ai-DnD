# 📋 Матрица версий компонентов

Этот документ фиксирует правильные версии компонентов для обеспечения стабильной работы RAG-сервиса.

## 🔄 Основная матрица совместимости

| Компонент | Версия | Примечание |
|----------|-------|-----------|
| **Python** | 3.11 | Обязательная версия для совместимости с PyTorch |
| **torch** | 2.7.1+cu126 | Специфическая сборка для CUDA 12.6 |
| **torchvision** | 0.22.1+cu126 | Совместимая версия с torch |
| **torchaudio** | 2.7.1+cu126 | Совместимая версия с torch |
| **CUDA base image** | 12.6 | Версия образа nvidia/cuda |
| **sentence-transformers** | 2.2.x | Последняя совместимая версия |

## ⚠️ Важные замечания

1. **Жесткая привязка версий**:
   - Версия PyTorch + CUDA всегда жестко привязана к версии Python
   - Изменение одной версии требует проверки совместимости всех остальных

2. **Проблема с ensurepip в Ubuntu**:
   - ensurepip отключен для системного Python в Debian/Ubuntu
   - Вызов `python3.11 -m ensurepip` приводит к ошибке и прерыванию сборки

3. **Правильное решение**:
   - Установка пакета `python3-pip` через apt-get
   - Инициализация pip через `python3.11 -m pip install --upgrade pip setuptools wheel`
   - Использование `python3.11 -m pip` для всех операций с пакетами
   - Отказ от создания симлинков `/usr/bin/python`

## 🛠️ Рекомендации по установке

```dockerfile
# Установка Python и системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Инициализация pip для python3.11
&& python3.11 -m pip install --upgrade pip setuptools wheel

# Установка PyTorch с использованием pip от python3.11
RUN python3.11 -m pip install --no-cache-dir \
    torch==2.7.1+cu126 \
    torchvision==0.22.1+cu126 \
    torchaudio==2.7.1+cu126 \
    --index-url https://download.pytorch.org/whl/cu126
```

## 📌 Заключение

Данные версии протестированы и гарантируют стабильную работу RAG-сервиса. Любые изменения должны сопровождаться тщательным тестированием совместимости.