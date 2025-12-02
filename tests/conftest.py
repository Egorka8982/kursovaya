"""
Конфигурация для pytest тестов
"""
import pytest
import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def server_process():
    """Запускает сервер FastAPI для тестов"""
    import sys
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Проверяем что main.py существует
    main_py = os.path.join(project_root, "main.py")
    if not os.path.exists(main_py):
        raise FileNotFoundError(f"Файл main.py не найден в {project_root}. Убедитесь, что вы находитесь в корне проекта.")
    
    # Запускаем сервер через uvicorn напрямую
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8007"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root
        )
    except Exception as e:
        raise Exception(f"Не удалось запустить сервер: {e}. Убедитесь, что uvicorn установлен: pip install uvicorn")
    
    # Ждем пока сервер запустится (проверяем доступность)
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:8007/health", timeout=1)
            break
        except Exception as e:
            if attempt == max_attempts - 1:
                # Выводим ошибки сервера если не запустился
                stdout, stderr = process.communicate(timeout=1)
                error_msg = f"Сервер не запустился за {max_attempts * 0.5} секунд.\n"
                if stderr:
                    error_msg += f"Ошибки сервера: {stderr.decode('utf-8', errors='ignore')[:500]}\n"
                error_msg += f"Убедитесь, что:\n"
                error_msg += f"1. Все зависимости установлены: pip install -r requirements.txt\n"
                error_msg += f"2. Порт 8007 свободен\n"
                error_msg += f"3. Приложение запускается вручную: python main.py"
                raise Exception(error_msg)
            time.sleep(0.5)
    
    yield process
    
    # Останавливаем сервер после тестов
    try:
        process.terminate()
        process.wait(timeout=5)
    except:
        process.kill()


@pytest.fixture(scope="function")
def driver():
    """Создает и возвращает WebDriver для тестов"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без GUI (можно убрать для отладки)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Автоматическая установка ChromeDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        raise Exception(
            f"Не удалось создать WebDriver: {e}\n"
            f"Убедитесь, что:\n"
            f"1. Google Chrome установлен\n"
            f"2. webdriver-manager установлен: pip install webdriver-manager\n"
            f"3. Есть доступ в интернет для загрузки ChromeDriver"
        )
    
    driver.implicitly_wait(3)  # Уменьшаем implicit wait, используем explicit waits
    driver.set_page_load_timeout(30)  # Таймаут загрузки страницы (уменьшен для быстрого обнаружения проблем)
    driver.set_script_timeout(20)  # Таймаут для выполнения JavaScript
    
    yield driver
    
    try:
        driver.quit()
    except:
        pass  # Игнорируем ошибки при закрытии


@pytest.fixture(scope="function")
def base_url():
    """Базовый URL приложения"""
    return "http://localhost:8007"

