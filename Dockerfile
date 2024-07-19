# Используем базовый образ с Python
FROM python:3.9-slim

# Обновляем и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    openvpn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Устанавливаем необходимые Python пакеты (если есть requirements.txt)
# RUN pip install -r requirements.txt

# Устанавливаем логирование на stdout для Docker
ENV PYTHONUNBUFFERED=1

# Запускаем главный скрипт
CMD ["python", "main.py"]
