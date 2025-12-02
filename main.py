from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from db_con import Base, engine

from api import client_router, animal_router, doctor_router, procedure_router, treatment_router

app = FastAPI(
    title="Veterinary Service API",
    description="API for managing veterinary clinic operations",
    version="1.0.0"
)


# Создаём таблицы
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка static
os.makedirs("static", exist_ok=True)

# Подключаем static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем API роуты
app.include_router(client_router)
app.include_router(animal_router)
app.include_router(doctor_router)
app.include_router(procedure_router)
app.include_router(treatment_router)

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
