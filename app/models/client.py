from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_name = Column(String(20), index=True, nullable=False)
    client_phone = Column(String(13), unique=True, index=True, nullable=False)

    # Связь с процедурами
    procedures = relationship("Procedure", back_populates="client")

