"""
Pydantic schemas for DoctorPatientAssignment.
"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class AssignmentCreate(BaseModel):
    """Schema for creating a doctor-patient assignment."""
    doctor_id: str
    patient_id: str
    notes: Optional[str] = None


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment."""
    status: Optional[str] = None
    notes: Optional[str] = None


class AssignmentOut(BaseModel):
    """Schema for returning an assignment."""
    id: PyObjectId
    doctor_id: str
    patient_id: str
    assigned_by: str
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True