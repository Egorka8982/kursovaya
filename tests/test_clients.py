"""
Тесты для страницы клиентов
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TestClients:
    """Тесты функциональности клиентов"""
    
    def test_open_clients_page(self, driver, base_url, server_process):
        """Тест открытия страницы клиентов"""
        driver.get(f"{base_url}/client")
        
        # Проверяем заголовок страницы
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Клиенты')]"))
        )
        assert title is not None
        
    def test_add_client(self, driver, base_url, server_process):
        """Тест добавления нового клиента"""
        # server_process фикстура гарантирует что сервер запущен
        driver.get(f"{base_url}/client")
        
        # Ждем загрузки страницы и JavaScript
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Клиенты')]"))
        )
        # Ждем загрузки таблицы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableBody"))
        )
        time.sleep(1)  # Дополнительная задержка для загрузки JS
        
        # Находим кнопку "Добавить" - используем более надежный селектор
        add_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
        )
        # Прокручиваем к кнопке если нужно
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(0.5)
        add_button.click()
        
        # Ждем открытия модального окна - Bootstrap Modal API
        # Проверяем что модальное окно видимо (display != none)
        try:
            modal = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.ID, "modal"))
            )
        except:
            # Альтернативная проверка - просто наличие элемента
            modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "modal"))
            )
        
        # Дополнительная проверка что форма внутри модального окна видима
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "form"))
        )
        time.sleep(0.5)  # Небольшая задержка для полной анимации
        
        # Ждем появления полей формы
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "client_name"))
        )
        name_input.clear()
        name_input.send_keys("Тестовый Клиент")
        
        phone_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "client_phone"))
        )
        phone_input.clear()
        phone_input.send_keys("+79991234567")
        
        # Отправляем форму
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()
        
        # Ждем закрытия модального окна
        # Проверяем что модальное окно скрыто (не видимо)
        try:
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located((By.ID, "modal"))
            )
        except:
            # Альтернативная проверка - просто ждем немного и проверяем что форма исчезла
            time.sleep(2)
            try:
                form = driver.find_element(By.ID, "form")
                if form and form.is_displayed():
                    time.sleep(2)  # Дополнительное ожидание
            except:
                pass  # Форма уже скрыта или не найдена
        
        # Ждем обновления таблицы - проверяем что данные загрузились
        WebDriverWait(driver, 10).until(
            lambda d: "Тестовый Клиент" in d.find_element(By.ID, "tableBody").text
        )

