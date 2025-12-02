from pydantic import BaseModel


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

