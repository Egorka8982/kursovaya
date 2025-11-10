from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db_con import get_db
import models
import scheme

# Роутеры для каждой таблицы
client_router = APIRouter(prefix="/clients", tags=["Clients"])
animal_router = APIRouter(prefix="/animals", tags=["Animals"])
doctor_router = APIRouter(prefix="/doctors", tags=["Doctors"])
treatment_router = APIRouter(prefix="/treatments", tags=["Treatments"])
procedure_router = APIRouter(prefix="/procedures", tags=["Procedures"])


# Client Routes
@client_router.post("/", response_model=scheme.Client)
def create_client(client: scheme.ClientCreate, db: Session = Depends(get_db)):
    """Добавление нового клиента"""
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@client_router.get("/", response_model=List[scheme.Client])
def get_clients(db: Session = Depends(get_db)):
    """Получение всех клиентов"""
    return db.query(models.Client).all()


@client_router.get("/{client_id}", response_model=scheme.Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Получение клиента по ID"""
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@client_router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Удаление клиента по ID"""
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}


# Animal Routes
@animal_router.post("/", response_model=scheme.Animal)
def create_animal(animal: scheme.AnimalCreate, db: Session = Depends(get_db)):
    """Добавление нового животного"""
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


@animal_router.get("/", response_model=List[scheme.Animal])
def get_animals(db: Session = Depends(get_db)):
    """Получение всех животных"""
    return db.query(models.Animal).all()


@animal_router.get("/{animal_id}", response_model=scheme.Animal)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    """Получение животного по ID"""
    animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@animal_router.delete("/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    """Удаление животного по ID"""
    animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"message": "Animal deleted successfully"}


# AnimalDoctor Routes
@doctor_router.post("/", response_model=scheme.AnimalDoctor)
def create_doctor(doctor: scheme.AnimalDoctorCreate, db: Session = Depends(get_db)):
    """Добавление нового врача"""
    db_doctor = models.AnimalDoctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@doctor_router.get("/", response_model=List[scheme.AnimalDoctor])
def get_doctors(db: Session = Depends(get_db)):
    """Получение всех врачей"""
    return db.query(models.AnimalDoctor).all()


@doctor_router.get("/{doctor_id}", response_model=scheme.AnimalDoctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Получение врача по ID"""
    doctor = db.query(models.AnimalDoctor).filter(models.AnimalDoctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@doctor_router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Удаление врача по ID"""
    doctor = db.query(models.AnimalDoctor).filter(models.AnimalDoctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}


# Treatment Routes
@treatment_router.post("/", response_model=scheme.TreatmentResponse)
def create_treatment(treatment: scheme.TreatmentCreate, db: Session = Depends(get_db)):
    """Добавление нового лечения"""
    db_treatment = models.Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


@treatment_router.get("/", response_model=List[scheme.TreatmentResponse])
def get_treatments(db: Session = Depends(get_db)):
    """Получение всех видов лечения"""
    return db.query(models.Treatment).all()


@treatment_router.get("/{treatment_id}", response_model=scheme.TreatmentResponse)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Получение вида лечения по ID"""
    treatment = db.query(models.Treatment).filter(models.Treatment.treatment_id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment


@treatment_router.delete("/{treatment_id}")
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Удаление вида лечения по ID"""
    treatment = db.query(models.Treatment).filter(models.Treatment.treatment_id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted successfully"}


# Procedure Routes
@procedure_router.post("/", response_model=scheme.Procedure)
def create_procedure(procedure: scheme.ProcedureCreate, db: Session = Depends(get_db)):
    """Добавление новой процедуры"""
    db_procedure = models.Procedure(**procedure.dict())
    db.add(db_procedure)
    db.commit()
    db.refresh(db_procedure)
    return db_procedure


@procedure_router.get("/", response_model=List[scheme.Procedure])
def get_procedures(db: Session = Depends(get_db)):
    """Получение всех процедур"""
    return db.query(models.Procedure).all()


@procedure_router.get("/{procedure_id}", response_model=scheme.Procedure)
def get_procedure(procedure_id: int, db: Session = Depends(get_db)):
    """Получение процедуры по ID"""
    procedure = db.query(models.Procedure).filter(models.Procedure.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure


@procedure_router.delete("/{procedure_id}")
def delete_procedure(procedure_id: int, db: Session = Depends(get_db)):
    """Удаление процедуры по ID"""
    procedure = db.query(models.Procedure).filter(models.Procedure.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    db.delete(procedure)
    db.commit()
    return {"message": "Procedure deleted successfully"}