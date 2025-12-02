from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.treatment import Treatment
from app.schemas.treatment import TreatmentResponse, TreatmentCreate

router = APIRouter(prefix="/treatments", tags=["Treatments"])


@router.post("/", response_model=TreatmentResponse)
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    """Добавление нового лечения"""
    db_treatment = Treatment(**treatment.model_dump())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


@router.get("/", response_model=List[TreatmentResponse])
def get_treatments(db: Session = Depends(get_db)):
    """Получение всех видов лечения"""
    return db.query(Treatment).all()


@router.get("/{treatment_id}", response_model=TreatmentResponse)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Получение вида лечения по ID"""
    treatment = db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment


@router.delete("/{treatment_id}")
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Удаление вида лечения по ID"""
    treatment = db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted successfully"}

