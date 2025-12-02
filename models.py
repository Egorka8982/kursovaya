from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_con import Base


class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_name = Column(String(20), index=True, nullable=False)
    client_phone = Column(String(13), unique=True, index=True, nullable=False)

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="client")


class Animal(Base):
    __tablename__ = "animal"

    animal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    animal_type = Column(String(20), nullable=False)  # Вид животного
    breed = Column(String(20), nullable=False)        # Порода
    name = Column(String(20), nullable=False)         # Кличка
    diagnosis = Column(String(100))                   # Диагноз

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="animal")


class AnimalDoctor(Base):
    __tablename__ = "animal_doctor"

    doctor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_name = Column(String(20), index=True, nullable=False)
    specialization = Column(String(20))
    doctor_phone = Column(String(13), unique=True, index=True)

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="doctor")


class Treatment(Base):
    __tablename__ = 'treatment'

    treatment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    treatment_name = Column(String(50), index=True, nullable=False)

    # Связь с процедурами
    procedures = relationship('Procedure', back_populates="treatment")


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

    # 🔥 FK на лечение — ЭТО ТОГО, ЧЕГО НЕ ХВАТАЛО!
    treatment_id = Column(Integer, ForeignKey("treatment.treatment_id"))

    # Связи
    client = relationship("Client", back_populates="procedures")
    animal = relationship("Animal", back_populates="procedures")
    doctor = relationship("AnimalDoctor", back_populates="procedures")
    treatment = relationship("Treatment", back_populates="procedures")
