from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Treatment(Base):
    __tablename__ = 'treatment'

    treatment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    treatment_name = Column(String(50), index=True, nullable=False)

    # Связь с процедурами
    procedures = relationship('Procedure', back_populates="treatment")

