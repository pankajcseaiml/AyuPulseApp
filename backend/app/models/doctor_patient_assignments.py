"""
MongoDB DoctorPatientAssignment model using Beanie.
"""
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field

class DoctorPatientAssignment(Document):
    doctor_id: Indexed(str)  # type: ignore
    patient_id: Indexed(str)  # type: ignore
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
