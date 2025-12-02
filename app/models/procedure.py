from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Procedure(Base):
    __tablename__ = "procedure"

    procedure_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK на клиента
    client_id = Column(Integer, ForeignKey("client.client_id"))
    client_name = Column(String(20))  # Дублируем имя для отображения (необязательно)

    # FK на животное
    animal_id = Column(Integer, ForeignKey("animal.animal_id"))
    animal_name = Column(String(20))  # Дублируем кличку животного

    # FK на доктора
    doctor_id = Column(Integer, ForeignKey("animal_doctor.doctor_id"))
    doctor_name = Column(String(20))  # Дублируем ФИО врача

    # FK на лечение
    treatment_id = Column(Integer, ForeignKey("treatment.treatment_id"))

    # Связи
    client = relationship("Client", back_populates="procedures")
    animal = relationship("Animal", back_populates="procedures")
    doctor = relationship("AnimalDoctor", back_populates="procedures")
    treatment = relationship("Treatment", back_populates="procedures")

