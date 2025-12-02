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
    
    # Запускаем сервер через uvicorn напрямую
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8007"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_root
    )
    
    # Ждем пока сервер запустится (проверяем доступность)
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:8007/health", timeout=1)
            break
        except:
            time.sleep(0.5)
    else:
        raise Exception("Сервер не запустился за отведенное время")
    
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
    
    # Автоматическая установка ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)  # Уменьшаем implicit wait, используем explicit waits
    driver.set_page_load_timeout(30)  # Таймаут загрузки страницы
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """Базовый URL приложения"""
    return "http://localhost:8007"

