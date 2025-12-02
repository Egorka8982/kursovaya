"""
Скрипт для отладки запуска сервера
Запустите этот файл чтобы проверить, запускается ли сервер вручную
"""
import subprocess
import sys
import time
import urllib.request

print("Попытка запуска сервера...")

try:
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8007"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("Процесс запущен, ждем 3 секунды...")
    time.sleep(3)
    
    # Проверяем статус процесса
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print(f"❌ Сервер завершился с кодом: {process.returncode}")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
    else:
        print("✅ Процесс работает, проверяем доступность...")
        
        # Проверяем доступность
        try:
            response = urllib.request.urlopen("http://localhost:8007/health", timeout=2)
            print(f"✅ Сервер доступен! Ответ: {response.read().decode()}")
        except Exception as e:
            print(f"❌ Сервер не отвечает: {e}")
        
        # Останавливаем
        process.terminate()
        process.wait(timeout=5)
        print("Сервер остановлен")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")

