"""
Pydantic schemas for Profile.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime

class LifestyleSchema(BaseModel):
    smoking: bool
    alcohol: bool
    exercise_frequency: str
    diet_type: str

class MedicalHistorySchema(BaseModel):
    diabetes: bool
    hypertension: bool
    previous_heart_disease: bool
    family_heart_history: bool
    current_medications: List[str]

class ProfileCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    height_cm: float
    weight_kg: float
    blood_group: str
    contact_number: str
    emergency_contact: str
    address: str
    occupation: str
    lifestyle: LifestyleSchema
    medical_history: MedicalHistorySchema

class ProfileUpdate(ProfileCreate):
    pass

from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProfileOut(ProfileCreate):
    id: PyObjectId
    user_id: PyObjectId
    age: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
