from pydantic import BaseModel


class TreatmentBase(BaseModel):
    treatment_name: str


class TreatmentCreate(TreatmentBase):
    pass


class TreatmentResponse(TreatmentBase):
    treatment_id: int

    class Config:
        from_attributes = True

