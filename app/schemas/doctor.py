from pydantic import BaseModel


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

