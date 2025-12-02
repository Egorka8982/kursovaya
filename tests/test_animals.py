"""
Тесты для страницы животных
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAnimals:
    """Тесты функциональности животных"""
    
    def test_open_animals_page(self, driver, base_url, server_process):
        """Тест открытия страницы животных"""
        # Проверяем что сервер доступен
        import urllib.request
        try:
            urllib.request.urlopen(f"{base_url}/health", timeout=2)
        except:
            pytest.fail("Сервер не доступен. Убедитесь что сервер запущен.")
        
        # Загружаем страницу с обработкой таймаутов
        try:
            driver.get(f"{base_url}/animal")
        except Exception as e:
            pytest.fail(f"Не удалось загрузить страницу: {e}")
        
        # Проверяем заголовок страницы
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Животные')]"))
        )
        assert title is not None
        
    def test_add_animal(self, driver, base_url, server_process):
        """Тест добавления нового животного"""
        # Проверяем что сервер доступен
        import urllib.request
        try:
            urllib.request.urlopen(f"{base_url}/health", timeout=2)
        except:
            pytest.fail("Сервер не доступен. Убедитесь что сервер запущен.")
        
        # Загружаем страницу с обработкой таймаутов
        try:
            driver.get(f"{base_url}/animal")
        except Exception as e:
            pytest.fail(f"Не удалось загрузить страницу: {e}")
        
        # Ждем загрузки страницы и JavaScript
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Животные')]"))
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
            EC.presence_of_element_located((By.ID, "animal_type"))
        )
        
        # Заполняем форму
        animal_type = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "animal_type"))
        )
        animal_type.clear()
        animal_type.send_keys("Собака")
        
        breed = driver.find_element(By.ID, "breed")
        breed.clear()
        breed.send_keys("Лабрадор")
        
        name = driver.find_element(By.ID, "name")
        name.clear()
        name.send_keys("Бобик")
        
        diagnosis = driver.find_element(By.ID, "diagnosis")
        diagnosis.clear()
        diagnosis.send_keys("Здоров")
        
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
        
        # Проверяем, что животное добавлено
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableBody"))
        )
        assert "Бобик" in table_body.text or "Собака" in table_body.text
        
    def test_refresh_button(self, driver, base_url, server_process):
        """Тест кнопки обновления"""
        # Проверяем что сервер доступен
        import urllib.request
        try:
            urllib.request.urlopen(f"{base_url}/health", timeout=2)
        except:
            pytest.fail("Сервер не доступен. Убедитесь что сервер запущен.")
        
        # Загружаем страницу с обработкой таймаутов
        try:
            driver.get(f"{base_url}/animal")
        except Exception as e:
            pytest.fail(f"Не удалось загрузить страницу: {e}")
        
        # Ждем загрузки
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Животные')]"))
        )
        
        # Находим кнопку обновления
        refresh_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Обновить')]")
        assert refresh_button is not None
        
        # Кликаем на кнопку
        refresh_button.click()
        
        # Проверяем, что страница обновилась (таблица присутствует)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableBody"))
        )

