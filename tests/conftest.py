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
            cwd=project_root,
            text=False  # Получаем bytes для правильной декодировки
        )
    except FileNotFoundError:
        raise Exception(
            f"Не удалось найти Python или uvicorn.\n"
            f"Убедитесь, что:\n"
            f"1. Python установлен и доступен: {sys.executable}\n"
            f"2. uvicorn установлен: pip install uvicorn\n"
            f"3. Виртуальное окружение активировано"
        )
    except Exception as e:
        raise Exception(
            f"Не удалось запустить сервер: {e}\n"
            f"Убедитесь, что uvicorn установлен: pip install uvicorn"
        )
    
    # Ждем пока сервер запустится (проверяем доступность)
    max_attempts = 30
    import urllib.request
    for attempt in range(max_attempts):
        try:
            # Проверяем что процесс еще работает
            return_code = process.poll()
            if return_code is not None:
                # Процесс завершился - получаем ошибки
                try:
                    stdout, stderr = process.communicate(timeout=2)
                except:
                    stdout, stderr = b"", b""
                
                error_msg = f"\n{'='*60}\n"
                error_msg += f"СЕРВЕР НЕ ЗАПУСТИЛСЯ (код выхода: {return_code})\n"
                error_msg += f"{'='*60}\n"
                
                if stderr:
                    stderr_text = stderr.decode('utf-8', errors='ignore')
                    error_msg += f"\nОШИБКИ СЕРВЕРА:\n{stderr_text[:2000]}\n"
                
                if stdout:
                    stdout_text = stdout.decode('utf-8', errors='ignore')
                    error_msg += f"\nВЫВОД СЕРВЕРА:\n{stdout_text[:1000]}\n"
                
                error_msg += f"\n{'='*60}\n"
                error_msg += f"ЧТО ДЕЛАТЬ:\n"
                error_msg += f"1. Проверьте зависимости: pip install -r requirements.txt\n"
                error_msg += f"2. Запустите сервер вручную: python main.py\n"
                error_msg += f"3. Проверьте порт: netstat -ano | findstr :8007\n"
                error_msg += f"4. Запустите отладку: python tests/debug_server.py\n"
                error_msg += f"{'='*60}\n"
                
                raise Exception(error_msg)
            
            # Проверяем доступность сервера
            try:
                urllib.request.urlopen("http://localhost:8007/health", timeout=1)
                # Дополнительная задержка чтобы сервер точно был готов
                time.sleep(0.5)
                break
            except urllib.error.URLError:
                # Сервер еще не готов, продолжаем ждать
                pass
        except urllib.error.URLError:
            # Сервер еще не готов, продолжаем ждать
            if attempt == max_attempts - 1:
                # Выводим ошибки сервера если не запустился
                try:
                    stdout, stderr = process.communicate(timeout=1)
                except:
                    stdout, stderr = b"", b""
                error_msg = f"Сервер не запустился за {max_attempts * 0.5} секунд.\n"
                if stderr:
                    error_msg += f"Ошибки сервера: {stderr.decode('utf-8', errors='ignore')[:1000]}\n"
                if stdout:
                    error_msg += f"Вывод сервера: {stdout.decode('utf-8', errors='ignore')[:500]}\n"
                error_msg += f"Убедитесь, что:\n"
                error_msg += f"1. Все зависимости установлены: pip install -r requirements.txt\n"
                error_msg += f"2. Порт 8007 свободен\n"
                error_msg += f"3. Приложение запускается вручную: python main.py"
                raise Exception(error_msg)
            time.sleep(0.5)
        except Exception as e:
            if attempt == max_attempts - 1:
                raise Exception(f"Ошибка при проверке сервера: {e}")
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

