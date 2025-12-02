from app.schemas.client import Client, ClientCreate
from app.schemas.animal import Animal, AnimalCreate
from app.schemas.doctor import AnimalDoctor, AnimalDoctorCreate
from app.schemas.treatment import TreatmentResponse, TreatmentCreate
from app.schemas.procedure import Procedure, ProcedureCreate

__all__ = [
    "Client", "ClientCreate",
    "Animal", "AnimalCreate",
    "AnimalDoctor", "AnimalDoctorCreate",
    "TreatmentResponse", "TreatmentCreate",
    "Procedure", "ProcedureCreate"
]

