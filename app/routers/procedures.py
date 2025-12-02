from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.procedure import Procedure
from app.schemas.procedure import Procedure as ProcedureSchema, ProcedureCreate

router = APIRouter(prefix="/procedures", tags=["Procedures"])


@router.post("/", response_model=ProcedureSchema)
def create_procedure(procedure: ProcedureCreate, db: Session = Depends(get_db)):
    """Добавление новой процедуры"""
    db_procedure = Procedure(**procedure.model_dump())
    db.add(db_procedure)
    db.commit()
    db.refresh(db_procedure)
    return db_procedure


@router.get("/", response_model=List[ProcedureSchema])
def get_procedures(db: Session = Depends(get_db)):
    """Получение всех процедур"""
    return db.query(Procedure).all()


@router.get("/{procedure_id}", response_model=ProcedureSchema)
def get_procedure(procedure_id: int, db: Session = Depends(get_db)):
    """Получение процедуры по ID"""
    procedure = db.query(Procedure).filter(Procedure.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure


@router.delete("/{procedure_id}")
def delete_procedure(procedure_id: int, db: Session = Depends(get_db)):
    """Удаление процедуры по ID"""
    procedure = db.query(Procedure).filter(Procedure.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    db.delete(procedure)
    db.commit()
    return {"message": "Procedure deleted successfully"}

