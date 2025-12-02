from pydantic import BaseModel


class ClientBase(BaseModel):
    client_name: str
    client_phone: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    client_id: int

    class Config:
        from_attributes = True  # Для работы с ORM-объектами

