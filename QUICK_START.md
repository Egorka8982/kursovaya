# Быстрый старт (шпаргалка)

## Минимальные команды для запуска:

```bash
# 1. Клонировать
git clone https://github.com/Egorka8982/kursovaya.git
cd kursovaya

# 2. Создать venv
python -m venv venv

# 3. Активировать venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 4. Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 5. Запустить
python main.py
```

Откройте: http://localhost:8007

## Если не работает:

1. Проверьте что venv активирован: должно быть `(venv)` в начале строки
2. Проверьте что все установилось: `pip list | findstr fastapi` (Windows) или `pip list | grep fastapi` (Linux/Mac)
3. Попробуйте запустить вручную: `python main.py`
4. Смотрите подробную инструкцию: [SETUP.md](SETUP.md)

## Для тестов:

1. Убедитесь что приложение запускается (`python main.py`)
2. Установите Google Chrome
3. Закройте приложение (Ctrl+C)
4. Запустите: `pytest tests/ -v`

