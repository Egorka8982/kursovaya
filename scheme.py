from pydantic import BaseModel
from typing import Optional


# Client Schemas
class ClientBase(BaseModel):
    client_name: str
    client_phone: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    client_id: int

    class Config:
        from_attributes = True  # Для работы с ORM-объектами


# Animal Schemas
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


# AnimalDoctor Schemas
class AnimalDoctorBase(BaseModel):
    doctor_name: str      # ФИО врача
    specialization: str   # Специализация
    doctor_phone: str     # Телефон


class AnimalDoctorCreate(AnimalDoctorBase):
    pass


class AnimalDoctor(AnimalDoctorBase):
    doctor_id: int

    class Config:
        from_attributes = True


#Tretment Shemas
class TreatmenеtBase(BaseModel):
    treatment_name: str

class TreatmentCreate(TreatmenеtBase):
    pass

class TreatmentResponse(TreatmenеtBase):
    treatment_id: int

    class Config:
        from_attributes = True


# Procedure Schemas
class ProcedureBase(BaseModel):
    client_id: int      # Внешний ключ на клиента
    client_name: str    # Дублирование имени для быстрого доступа
    animal_id: int      # Внешний ключ на животное
    animal_name: str    # Дублирование клички
    doctor_id: int      # Внешний ключ на врача
    doctor_name: str    # Дублирование ФИО врача


class ProcedureCreate(ProcedureBase):
    pass


class Procedure(ProcedureBase):
    procedure_id: int   # Первичный ключ

    class Config:
        from_attributes = True