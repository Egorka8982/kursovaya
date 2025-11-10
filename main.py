from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import os
from api import client_router, animal_router, doctor_router, procedure_router, treatment_router

app = FastAPI(
    title="Veterinary Service API",
    description="API for managing veterinary clinic operations",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем папки если их нет
os.makedirs("static", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем все роутеры API
app.include_router(client_router)
app.include_router(animal_router)
app.include_router(doctor_router)
app.include_router(procedure_router)
app.include_router(treatment_router)

# HTML страницы
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница"""
    try:
        return FileResponse('static/index.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Главная страница</h1><p>HTML файл не найден</p>")

@app.get("static/client", response_class=HTMLResponse)
async def clients_page():
    """Страница управления клиентами"""
    try:
        return FileResponse('static/client.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Клиенты</h1><p>HTML файл не найден</p>")

@app.get("static/animal", response_class=HTMLResponse)
async def animals_page():
    """Страница управления животными"""
    try:
        return FileResponse('static/animal.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Животные</h1><p>HTML файл не найден</p>")

@app.get("static/doctors-page", response_class=HTMLResponse)
async def doctors_page():
    """Страница управления врачами"""
    try:
        return FileResponse('static/animal_doctor.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Врачи</h1><p>HTML файл не найден</p>")

@app.get("static/treatments-page", response_class=HTMLResponse)
async def treatments_page():
    """Страница управления видами лечения"""
    try:
        return FileResponse('static/treatment.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Виды лечения</h1><p>HTML файл не найден</p>")

@app.get("static/procedures-page", response_class=HTMLResponse)
async def procedures_page():
    """Страница управления процедурами"""
    try:
        return FileResponse('static/procedure.html')
    except FileNotFoundError:
        return HTMLResponse("<h1>Процедуры</h1><p>HTML файл не найден</p>")

@app.get("/health")
def health_check():
    """Проверка статуса API"""
    return {"status": "healthy"}

@app.get("/api-test")
def api_test():
    """Тестовый эндпоинт для проверки API"""
    return {"message": "API работает корректно"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True
    )