"""
Pydantic schemas for Patient.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime
from .profile import MedicalHistorySchema

class PatientCreate(BaseModel):
    full_name: str
    relationship: str
    date_of_birth: date
    gender: str
    blood_group: str
    medical_history: MedicalHistorySchema
    notes: Optional[str] = None

class PatientUpdate(PatientCreate):
    pass

from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class PatientOut(PatientCreate):
    id: PyObjectId
    owner_id: PyObjectId
    age: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True