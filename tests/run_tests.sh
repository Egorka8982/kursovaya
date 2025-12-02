#!/bin/bash
# Скрипт для запуска тестов на Linux/Mac

echo "Установка зависимостей..."
pip install -r requirements.txt

echo ""
echo "Запуск тестов..."
pytest tests/ -v

