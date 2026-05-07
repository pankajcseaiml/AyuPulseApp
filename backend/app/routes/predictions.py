from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
import json
import os
import shutil
import uuid
from datetime import datetime
from app.models.prediction import Prediction
from app.models.patient import Patient
from app.models.profile import UserProfile
from app.models.user import User
from app.schemas.prediction import PredictionOut
from app.routes.auth import get_current_user
from app.schemas.response import StandardResponse
from app.services.prediction_service import run_prediction
from app.core.config import settings

router = APIRouter()

async def save_upload_file(upload_file: UploadFile, prefix: str) -> str:
    if not upload_file:
        return None
    try:
        filename = f"{prefix}_{uuid.uuid4().hex[:8]}_{upload_file.filename}"
        filepath = os.path.join(settings.UPLOAD_DIR, prefix, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return filepath
    except Exception as e:
        print(f"Error saving {prefix} file: {e}")
        return None

@router.post("", response_model=StandardResponse[PredictionOut])
async def create_prediction(
    clinical_data: str = Form(...),
    patient_id: Optional[str] = Form(None),
    xray_file: Optional[UploadFile] = File(None),
    ecg_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user)
):
    try:
        clinical_dict = json.loads(clinical_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in clinical_data")
        
    subject_name = current_user.name
    if patient_id:
        try:
            patient = await Patient.get(patient_id)
            if not patient or patient.owner_id != str(current_user.id):
                raise HTTPException(status_code=404, detail="Patient not found")
            subject_name = patient.full_name
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid patient ID")
    else:
        profile = await UserProfile.find_one(UserProfile.user_id == str(current_user.id))
        if profile:
            subject_name = profile.full_name
            
    # Save files
    xray_path = await save_upload_file(xray_file, "xray") if xray_file and xray_file.filename else None
    ecg_path = await save_upload_file(ecg_file, "ecg") if ecg_file and ecg_file.filename else None
    
    # Run pipeline
    try:
        result = await run_prediction(clinical_dict, xray_path, ecg_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
        
    # Save prediction
    new_prediction = Prediction(
        user_id=str(current_user.id),
        patient_id=patient_id,
        subject_name=subject_name,
        
        # Clinical inputs
        gender=clinical_dict["gender"],
        age=clinical_dict["age"],
        currentSmoker=clinical_dict["currentSmoker"],
        cigsPerDay=clinical_dict.get("cigsPerDay", 0),
        BPMeds=clinical_dict["BPMeds"],
        prevalentStroke=clinical_dict["prevalentStroke"],
        prevalentHyp=clinical_dict["prevalentHyp"],
        diabetes=clinical_dict["diabetes"],
        totChol=clinical_dict["totChol"],
        sysBP=clinical_dict["sysBP"],
        diaBP=clinical_dict["diaBP"],
        BMI=clinical_dict["BMI"],
        heartRate=clinical_dict["heartRate"],
        glucose=clinical_dict["glucose"],
        CP=clinical_dict["CP"],
        
        xray_original_path=xray_path,
        ecg_original_path=ecg_path,
        xray_analysis=result.pop('xray_analysis', None),
        ecg_analysis=result.pop('ecg_analysis', None),
        
        **result
    )
    
    await new_prediction.insert()
    
    return StandardResponse(
        success=True,
        message="Prediction completed",
        data=PredictionOut(**new_prediction.model_dump())
    )

@router.get("", response_model=StandardResponse[List[PredictionOut]])
async def list_predictions(current_user: User = Depends(get_current_user)):
    predictions = await Prediction.find(Prediction.user_id == str(current_user.id)).sort("-created_at").to_list()
    data = [PredictionOut(**p.model_dump()) for p in predictions]
    return StandardResponse(success=True, message="Predictions retrieved", data=data)

@router.get("/stats/summary", response_model=StandardResponse[dict])
async def get_prediction_stats(current_user: User = Depends(get_current_user)):
    predictions = await Prediction.find(Prediction.user_id == str(current_user.id)).sort("-created_at").to_list()
    
    total = len(predictions)
    high_risk = sum(1 for p in predictions if p.risk_category == "High")
    
    last_score = predictions[0].risk_score * 100 if predictions else 0
    
    days_since_last = 0
    if predictions:
        latest = predictions[0].created_at
        days_since_last = (datetime.utcnow() - latest).days
        
    return StandardResponse(
        success=True,
        message="Stats retrieved",
        data={
            "total_predictions": total,
            "high_risk_alerts": high_risk,
            "last_risk_score": float(last_score),
            "days_since_last": days_since_last,
            "history": [{"date": p.created_at.isoformat(), "score": p.risk_score * 100} for p in predictions[:5]]
        }
    )

@router.get("/patient/{patient_id}", response_model=StandardResponse[List[PredictionOut]])
async def list_patient_predictions(patient_id: str, current_user: User = Depends(get_current_user)):
    predictions = await Prediction.find(
        Prediction.user_id == str(current_user.id),
        Prediction.patient_id == patient_id
    ).sort("-created_at").to_list()
    data = [PredictionOut(**p.model_dump()) for p in predictions]
    return StandardResponse(success=True, message="Predictions retrieved", data=data)

@router.get("/{prediction_id}", response_model=StandardResponse[PredictionOut])
async def get_prediction(prediction_id: str, current_user: User = Depends(get_current_user)):
    try:
        prediction = await Prediction.get(prediction_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid prediction ID")
        
    if not prediction or prediction.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    return StandardResponse(
        success=True,
        message="Prediction retrieved",
        data=PredictionOut(**prediction.model_dump())
    )

@router.delete("/{prediction_id}", response_model=StandardResponse[None])
async def delete_prediction(prediction_id: str, current_user: User = Depends(get_current_user)):
    try:
        prediction = await Prediction.get(prediction_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid prediction ID")
        
    if not prediction or prediction.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    # Delete files
    for path in [prediction.xray_original_path, prediction.xray_gradcam_path, prediction.ecg_original_path, prediction.ecg_gradcam_path]:
        if path and os.path.exists(path):
            try: os.remove(path)
            except: pass
            
    await prediction.delete()
    return StandardResponse(success=True, message="Prediction deleted successfully", data=None)