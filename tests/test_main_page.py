"""
Тесты для главной страницы
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMainPage:
    """Тесты главной страницы"""
    
    def test_open_main_page(self, driver, base_url, server_process):
        """Тест открытия главной страницы"""
        driver.get(base_url)
        
        # Проверяем заголовок
        title = driver.find_element(By.TAG_NAME, "h1")
        assert "Добро пожаловать" in title.text
        
        # Проверяем наличие навигации
        sidebar = driver.find_element(By.CLASS_NAME, "sidebar")
        assert sidebar is not None
        
    def test_navigation_links(self, driver, base_url, server_process):
        """Тест навигационных ссылок"""
        driver.get(base_url)
        
        # Проверяем ссылки в сайдбаре
        links = driver.find_elements(By.CSS_SELECTOR, ".sidebar a")
        assert len(links) >= 5  # Должно быть минимум 5 ссылок
        
        # Проверяем наличие ссылок на основные разделы
        link_texts = [link.text for link in links]
        assert "Клиенты" in link_texts
        assert "Животные" in link_texts
        assert "Врачи" in link_texts
        
    def test_navigate_to_clients(self, driver, base_url, server_process):
        """Тест перехода на страницу клиентов"""
        driver.get(base_url)
        
        # Находим и кликаем на ссылку "Клиенты"
        client_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Клиенты')]"))
        )
        client_link.click()
        
        # Проверяем, что перешли на страницу клиентов
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Клиенты')]"))
        )
        
        assert "/client" in driver.current_url or "client" in driver.current_url.lower()

