# Используем легкий базовый образ Python 3.13
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости без кэша (для уменьшения размера образа)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код бота
COPY bot.py .

# Команда запуска бота при старте контейнера
CMD ["python", "bot.py"]
