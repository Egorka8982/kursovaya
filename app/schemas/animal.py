from pydantic import BaseModel


class AnimalBase(BaseModel):
    animal_type: str  # Вид животного
    breed: str        # Порода
    name: str         # Кличка
    diagnosis: str    # Диагноз


class AnimalCreate(AnimalBase):
    pass


class Animal(AnimalBase):
    animal_id: int

    class Config:
        from_attributes = True

