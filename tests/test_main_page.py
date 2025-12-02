"""
Тесты для главной страницы
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMainPage:
    """Тесты главной страницы"""
    
    def test_open_main_page(self, driver, base_url, server_process):
        """Тест открытия главной страницы"""
        # server_process фикстура гарантирует что сервер запущен
        driver.get(base_url)
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)  # Дополнительная задержка для загрузки контента
        
        # Проверяем заголовок
        title = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "Добро пожаловать" in title.text
        
        # Проверяем наличие навигации
        sidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sidebar"))
        )
        assert sidebar is not None
        
    def test_navigation_links(self, driver, base_url, server_process):
        """Тест навигационных ссылок"""
        # server_process фикстура гарантирует что сервер запущен
        driver.get(base_url)
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
        
        # Проверяем ссылки в сайдбаре
        links = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sidebar a"))
        )
        assert len(links) >= 5  # Должно быть минимум 5 ссылок
        
        # Проверяем наличие ссылок на основные разделы
        link_texts = [link.text for link in links]
        assert "Клиенты" in link_texts
        assert "Животные" in link_texts
        assert "Врачи" in link_texts
        
    def test_navigate_to_clients(self, driver, base_url, server_process):
        """Тест перехода на страницу клиентов"""
        # server_process фикстура гарантирует что сервер запущен
        driver.get(base_url)
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
        
        # Находим и кликаем на ссылку "Клиенты"
        client_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Клиенты')]"))
        )
        client_link.click()
        
        # Проверяем, что перешли на страницу клиентов
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Клиенты')]"))
        )
        
        assert "/client" in driver.current_url or "client" in driver.current_url.lower()

