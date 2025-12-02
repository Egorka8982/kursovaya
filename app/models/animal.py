from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Animal(Base):
    __tablename__ = "animal"

    animal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_type = Column(String(20), nullable=False)  # Вид животного
    breed = Column(String(20), nullable=False)        # Порода
    name = Column(String(20), nullable=False)         # Кличка
    diagnosis = Column(String(100))                   # Диагноз

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="animal")

