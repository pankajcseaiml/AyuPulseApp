"""
MongoDB DoctorPatientAssignment model using Beanie.
"""
from datetime import datetime
from typing import Optional, Annotated
from beanie import Document
from beanie.odm.fields import Indexed
from pydantic import Field

class DoctorPatientAssignment(Document):
    doctor_id: Annotated[str, Indexed()]
    patient_id: Annotated[str, Indexed()]
    assigned_by: str
    status: str = "active"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "doctor_patient_assignments"
        indexes = [
            ["doctor_id", "patient_id"]
        ]
