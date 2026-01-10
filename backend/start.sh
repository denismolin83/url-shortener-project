#!/bin/sh
set -e

# Печатаем текущую директорию и список файлов для отладки (увидите в логах)
echo "Текущая директория: $(pwd)"
ls -la

echo "Применение миграций базы данных..."
# Флаг -c указывает путь к конфигу явно
alembic -c alembic.ini upgrade head

echo "Запуск FastAPI сервера..."
exec uvicorn main:app --host 0.0.0.0 --port 8000