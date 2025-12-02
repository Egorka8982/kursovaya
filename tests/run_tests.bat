@echo off
REM Скрипт для запуска тестов на Windows

echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Запуск тестов...
pytest tests/ -v

pause

