"""
MongoDB UserProfile model using Beanie.
"""
from datetime import datetime, date
from typing import Optional, List, Annotated
from beanie import Document
from beanie.odm.fields import Indexed
from pydantic import BaseModel, Field

class Lifestyle(BaseModel):
    smoking: bool = False
    alcohol: bool = False
    exercise_frequency: str = "Never"  # "Never" / "Rarely" / "Weekly" / "Daily"
    diet_type: str = "Vegetarian"  # "Vegetarian" / "Non-Vegetarian" / "Vegan"

class MedicalHistory(BaseModel):
    diabetes: bool = False
    hypertension: bool = False
    previous_heart_disease: bool = False
    family_heart_history: bool = False
    current_medications: List[str] = Field(default_factory=list)

class UserProfile(Document):
    user_id: Annotated[str, Indexed(unique=True)]
    full_name: str
    date_of_birth: date
    age: int
    gender: str  # "Male" / "Female" / "Other"
    height_cm: float
    weight_kg: float
    blood_group: str
    contact_number: str
    emergency_contact: str
    address: str
    occupation: str
    lifestyle: Lifestyle
    medical_history: MedicalHistory
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "profiles"
