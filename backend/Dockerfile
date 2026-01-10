# Использование легковесного образа Python
FROM python:3.11-slim

# Установка системных зависимостей для сборки некоторых библиотек Python (если нужно)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Запрет Python создавать файлы кэша .pyc и включение немедленного вывода логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Сначала копируем только файл зависимостей для эффективного кэширования слоев Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код проекта
COPY . .

# Делаем скрипт запуска исполняемым (на случай, если права потерялись при копировании)
RUN chmod +x start.sh

# Открываем порт, на котором работает FastAPI
EXPOSE 8000

# Запускаем приложение через наш скрипт
CMD ["./start.sh"]