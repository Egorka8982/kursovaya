from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.doctor import AnimalDoctor
from app.schemas.doctor import AnimalDoctor as AnimalDoctorSchema, AnimalDoctorCreate

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=AnimalDoctorSchema)
def create_doctor(doctor: AnimalDoctorCreate, db: Session = Depends(get_db)):
    """Добавление нового врача"""
    db_doctor = AnimalDoctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.get("/", response_model=List[AnimalDoctorSchema])
def get_doctors(db: Session = Depends(get_db)):
    """Получение всех врачей"""
    return db.query(AnimalDoctor).all()


@router.get("/{doctor_id}", response_model=AnimalDoctorSchema)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Получение врача по ID"""
    doctor = db.query(AnimalDoctor).filter(AnimalDoctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Удаление врача по ID"""
    doctor = db.query(AnimalDoctor).filter(AnimalDoctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}

