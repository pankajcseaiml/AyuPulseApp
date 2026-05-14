from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate, PatientOut
from app.routes.auth import get_current_user
from app.schemas.response import StandardResponse, PaginatedResponse
from datetime import datetime

router = APIRouter()

@router.post("", response_model=StandardResponse[PatientOut])
async def create_patient(patient_data: PatientCreate, current_user: User = Depends(get_current_user)):
    today = datetime.today().date()
    dob = patient_data.date_of_birth
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    new_patient = Patient(
        owner_id=str(current_user.id),
        age=age,
        **patient_data.model_dump()
    )
    await new_patient.insert()
    
    return StandardResponse(
        success=True,
        message="Patient created successfully",
        data=PatientOut(**new_patient.model_dump())
    )

@router.get("", response_model=StandardResponse[List[PatientOut]])
async def list_patients(current_user: User = Depends(get_current_user)):
    patients = await Patient.find(Patient.owner_id == str(current_user.id)).to_list()
    
    data = [PatientOut(**p.model_dump()) for p in patients]
    
    return StandardResponse(
        success=True,
        message="Patients retrieved successfully",
        data=data
    )

@router.get("/{patient_id}", response_model=StandardResponse[PatientOut])
async def get_patient(patient_id: str, current_user: User = Depends(get_current_user)):
    try:
        patient = await Patient.get(patient_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")
        
    if not patient or patient.owner_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Patient not found")
        
    return StandardResponse(
        success=True,
        message="Patient retrieved",
        data=PatientOut(**patient.model_dump())
    )

@router.put("/{patient_id}", response_model=StandardResponse[PatientOut])
async def update_patient(patient_id: str, patient_update: PatientUpdate, current_user: User = Depends(get_current_user)):
    try:
        patient = await Patient.get(patient_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")
        
    if not patient or patient.owner_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Patient not found")
        
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(patient, key, value)
        
    if "date_of_birth" in update_data:
        today = datetime.today().date()
        dob = patient.date_of_birth
        patient.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
    patient.updated_at = datetime.utcnow()
    await patient.save()
    
    return StandardResponse(
        success=True,
        message="Patient updated successfully",
        data=PatientOut(**patient.model_dump())
    )

@router.get("/search", response_model=StandardResponse[List[PatientOut]])
async def search_patients(
    query: str = None,
    gender: str = None,
    min_age: int = None,
    max_age: int = None,
    current_user: User = Depends(get_current_user)
):
    """Search patients with filters."""
    from beanie.operators import RegEx
    
    # Build query filters
    filters = [Patient.owner_id == str(current_user.id)]
    
    if query:
        filters.append(RegEx(Patient.full_name, query, "i"))
    
    if gender:
        filters.append(Patient.gender == gender)
    
    if min_age is not None:
        filters.append(Patient.age >= min_age)
    
    if max_age is not None:
        filters.append(Patient.age <= max_age)
    
    patients = await Patient.find(*filters).to_list()
    data = [PatientOut(**p.model_dump()) for p in patients]
    
    return StandardResponse(
        success=True,
        message="Patients retrieved",
        data=data
    )

@router.get("/stats/summary", response_model=StandardResponse[dict])
async def get_patient_stats(current_user: User = Depends(get_current_user)):
    """Get patient statistics for the current user."""
    patients = await Patient.find(Patient.owner_id == str(current_user.id)).to_list()
    
    total = len(patients)
    male_count = sum(1 for p in patients if p.gender and p.gender.lower() == 'male')
    female_count = sum(1 for p in patients if p.gender and p.gender.lower() == 'female')
    average_age = sum(p.age for p in patients) / max(1, total)
    
    return StandardResponse(
        success=True,
        message="Stats retrieved",
        data={
            "total_patients": total,
            "male_count": male_count,
            "female_count": female_count,
            "average_age": round(average_age, 1),
            "high_risk_count": 0,
            "recent_patients": total
        }
    )

@router.delete("/{patient_id}", response_model=StandardResponse[None])
async def delete_patient(patient_id: str, current_user: User = Depends(get_current_user)):
    try:
        patient = await Patient.get(patient_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")
        
    if not patient or patient.owner_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Patient not found")
        
    await patient.delete()
    
    return StandardResponse(
        success=True,
        message="Patient deleted successfully",
        data=None
    )