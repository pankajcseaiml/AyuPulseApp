"""
MongoDB Patient model using Beanie.
"""
from datetime import datetime, date
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field
from .profile import MedicalHistory

class Patient(Document):
    owner_id: Indexed(str)  # type: ignore
    full_name: str
    relationship: str  # "Self" / "Spouse" / "Parent" / "Child" / "Sibling" / "Other"
    date_of_birth: date
    age: int
    gender: str
    blood_group: str
    medical_history: MedicalHistory
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "patients"