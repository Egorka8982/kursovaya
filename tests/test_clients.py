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
        driver.get(f"{base_url}/client")
        
        # Ждем загрузки страницы и JavaScript
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Клиенты')]"))
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
        
        # Ждем открытия модального окна
        modal = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "modal"))
        )
        # Дополнительная проверка что модальное окно видимо
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "modal"))
        )
        time.sleep(0.5)  # Небольшая задержка для полной анимации
        
        # Ждем появления полей формы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "client_name"))
        )
        
        # Заполняем форму
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "client_name"))
        )
        name_input.clear()
        name_input.send_keys("Тестовый Клиент")
        
        phone_input = driver.find_element(By.ID, "client_phone")
        phone_input.clear()
        phone_input.send_keys("+79991234567")
        
        # Отправляем форму
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()
        
        # Ждем закрытия модального окна
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal"))
        )
        
        # Ждем обновления таблицы
        time.sleep(2)
        
        # Проверяем, что клиент добавлен в таблицу
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableBody"))
        )
        assert "Тестовый Клиент" in table_body.text
        
    def test_view_clients_table(self, driver, base_url, server_process):
        """Тест просмотра таблицы клиентов"""
        driver.get(f"{base_url}/client")
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableBody"))
        )
        
        # Проверяем наличие таблицы
        table = driver.find_element(By.TAG_NAME, "table")
        assert table is not None
        
        # Проверяем заголовки таблицы
        headers = driver.find_elements(By.CSS_SELECTOR, "thead th")
        header_texts = [h.text for h in headers]
        assert "ID" in header_texts
        assert "Имя" in header_texts
        assert "Телефон" in header_texts

