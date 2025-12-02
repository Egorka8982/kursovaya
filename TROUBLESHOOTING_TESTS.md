# Решение проблем с тестами

## Проблема: "Сервер не доступен. Убедитесь что сервер запущен."

Если тесты падают с этой ошибкой, выполните следующие шаги:

### 1. Обновите код из репозитория

```bash
git pull origin main
```

Убедитесь, что у вас последняя версия кода.

### 2. Проверьте виртуальное окружение

**Windows:**
```powershell
# Активируйте venv
.\venv\Scripts\Activate.ps1

# Проверьте что Python правильный
python --version
where python  # Должен показать путь к venv\Scripts\python.exe
```

**Linux/Mac:**
```bash
source venv/bin/activate
python --version
which python  # Должен показать путь к venv/bin/python
```

### 3. Установите/обновите зависимости

```bash
pip install -r requirements.txt
```

Особенно важно:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic`

### 4. Проверьте что порт свободен

**Windows:**
```powershell
netstat -ano | findstr :8007
```

Если порт занят, либо:
- Закройте другой процесс на этом порту
- Или измените порт в `main.py` и `tests/conftest.py`

**Linux/Mac:**
```bash
lsof -i :8007
```

### 5. Запустите сервер вручную

```bash
python main.py
```

Если сервер не запускается, вы увидите ошибку. Исправьте её перед запуском тестов.

### 6. Запустите диагностический скрипт

```bash
python tests/debug_server.py
```

Этот скрипт покажет подробную информацию о проблеме.

### 7. Проверьте структуру проекта

Убедитесь что файлы на месте:
- `main.py` в корне проекта
- `app/` директория с модулями
- `tests/` директория с тестами

### 8. Запустите тесты с подробным выводом

```bash
pytest tests/ -v --tb=long
```

Флаг `-v` покажет подробный вывод, `--tb=long` покажет полный traceback ошибок.

## Частые проблемы

### Проблема: "ModuleNotFoundError: No module named 'app'"

**Решение:** Убедитесь что вы запускаете тесты из корня проекта:
```bash
cd C:\Users\ivan\PycharmProjects\kursovaya
pytest tests/
```

### Проблема: "Port 8007 is already in use"

**Решение:** 
1. Найдите процесс: `netstat -ano | findstr :8007`
2. Закройте его или измените порт

### Проблема: "ChromeDriver not found"

**Решение:**
```bash
pip install webdriver-manager
```

`webdriver-manager` автоматически скачает нужный ChromeDriver.

### Проблема: Тесты работают у одного, но не у другого

**Причины:**
1. Разные версии Python (нужен Python 3.8+)
2. Не установлены зависимости
3. Не активировано виртуальное окружение
4. Порт занят другим процессом
5. Старая версия кода

**Решение:** Выполните все шаги выше по порядку.

## Если ничего не помогает

1. Удалите виртуальное окружение и создайте заново:
```bash
# Windows
rmdir /s venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Linux/Mac
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Проверьте версию Python:
```bash
python --version  # Должно быть 3.8 или выше
```

3. Запустите тесты с отключенным headless режимом (чтобы видеть что происходит):
   - Откройте `tests/conftest.py`
   - Закомментируйте строку: `chrome_options.add_argument("--headless")`
   - Запустите тесты снова

