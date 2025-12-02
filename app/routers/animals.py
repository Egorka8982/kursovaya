from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.animal import Animal
from app.schemas.animal import Animal as AnimalSchema, AnimalCreate

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.post("/", response_model=AnimalSchema)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    """Добавление нового животного"""
    db_animal = Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


@router.get("/", response_model=List[AnimalSchema])
def get_animals(db: Session = Depends(get_db)):
    """Получение всех животных"""
    return db.query(Animal).all()


@router.get("/{animal_id}", response_model=AnimalSchema)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    """Получение животного по ID"""
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.delete("/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    """Удаление животного по ID"""
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"message": "Animal deleted successfully"}

