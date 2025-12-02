from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class AnimalDoctor(Base):
    __tablename__ = "animal_doctor"

    doctor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_name = Column(String(20), index=True, nullable=False)
    specialization = Column(String(20))
    doctor_phone = Column(String(13), unique=True, index=True)

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="doctor")

