// Общие функции для всех страниц

// Экранирование HTML
function esc(s) {
  return String(s || '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

// JSON строка для JS
function jsString(s) {
  return JSON.stringify(String(s || ''));
}

// Универсальная функция для работы с API
async function apiRequest(url, method = 'GET', data = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (data) options.body = JSON.stringify(data);
  
  try {
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Универсальная функция для создания/редактирования
async function saveEntity(apiUrl, id, data, modal, loadFn) {
  try {
    if (id) {
      // Редактирование: DELETE + POST (так как PUT не реализован в API)
      await apiRequest(apiUrl + id, 'DELETE');
      await apiRequest(apiUrl, 'POST', data);
    } else {
      // Создание
      await apiRequest(apiUrl, 'POST', data);
    }
    if (modal) modal.hide();
    loadFn();
  } catch (error) {
    alert('Ошибка сохранения');
  }
}

// Универсальная функция удаления
async function deleteEntity(apiUrl, id, name, loadFn) {
  if (!confirm(`Удалить ${name} #${id}?`)) return;
  try {
    await apiRequest(apiUrl + id, 'DELETE');
    loadFn();
  } catch (error) {
    alert('Ошибка удаления');
  }
}

