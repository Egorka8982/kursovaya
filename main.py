from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import clients, animals, doctors, treatments, procedures

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка static
os.makedirs("static", exist_ok=True)

# Подключаем static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем API роуты
app.include_router(clients.router)
app.include_router(animals.router)
app.include_router(doctors.router)
app.include_router(treatments.router)
app.include_router(procedures.router)

# ---------------------------
# HTML страницы
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def index_page():
    return FileResponse("static/index.html")


@app.get("/client", response_class=HTMLResponse)
async def client_page():
    return FileResponse("static/client.html")


@app.get("/animal", response_class=HTMLResponse)
async def animal_page():
    return FileResponse("static/animal.html")


@app.get("/doctor", response_class=HTMLResponse)
async def doctor_page():
    return FileResponse("static/animal_doctor.html")


@app.get("/treatment", response_class=HTMLResponse)
async def treatment_page():
    return FileResponse("static/treatment.html")


@app.get("/procedure", response_class=HTMLResponse)
async def procedure_page():
    return FileResponse("static/procedure.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api-test")
def api_test():
    return {"message": "API работает корректно"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True
    )

