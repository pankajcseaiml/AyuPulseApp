"""
Pydantic schemas for prediction requests and responses.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, field_serializer
from datetime import datetime
from app.models.prediction import ShapFeature, ReferenceRange

class ClinicalInput(BaseModel):
    gender: int
    age: int
    currentSmoker: int
    cigsPerDay: float
    BPMeds: int
    prevalentStroke: int
    prevalentHyp: int
    diabetes: int
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    heartRate: float
    glucose: float
    CP: int

from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class PredictionOut(BaseModel):
    id: PyObjectId
    user_id: PyObjectId
    patient_id: Optional[str]
    subject_name: str
    
    gender: int
    age: int
    currentSmoker: int
    cigsPerDay: float
    BPMeds: int
    prevalentStroke: int
    prevalentHyp: int
    diabetes: int
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    heartRate: float
    glucose: float
    CP: int
    
    xray_original_path: Optional[str]
    xray_gradcam_path: Optional[str]
    ecg_original_path: Optional[str]
    ecg_gradcam_path: Optional[str]
    
    risk_score: float
    risk_category: str
    confidence: float
    clinical_score: float
    xray_score: Optional[float]
    ecg_score: Optional[float]
    fusion_weights: Dict[str, float]
    modalities_used: List[str]
    xray_analysis: Optional[str] = None
    ecg_analysis: Optional[str] = None
    
    shap_features: List[ShapFeature]
    explanation_text: str
    risk_factors: List[str]
    recommendations: List[str]
    
    model_accuracy: float
    model_auc_roc: float
    model_precision: float
    model_recall: float
    model_f1: float
    
    # Store as dict internally but serialize as list
    clinical_reference_ranges: Dict[str, ReferenceRange]
    
    created_at: datetime
    prediction_duration_ms: int

    @field_serializer('clinical_reference_ranges')
    def serialize_clinical_reference_ranges(self, clinical_reference_ranges: Dict[str, ReferenceRange], _info) -> List[Dict[str, Any]]:
        """Transform clinical_reference_ranges dictionary into list format for frontend."""
        result = []
        for param_name, ref_range in clinical_reference_ranges.items():
            # Format reference range string
            if ref_range.normal_min is not None and ref_range.normal_max is not None:
                ref_range_str = f"{ref_range.normal_min}-{ref_range.normal_max} {ref_range.unit}"
            elif ref_range.normal_min is not None:
                ref_range_str = f"≥{ref_range.normal_min} {ref_range.unit}"
            elif ref_range.normal_max is not None:
                ref_range_str = f"≤{ref_range.normal_max} {ref_range.unit}"
            else:
                ref_range_str = "N/A"
            
            # Capitalize status for display
            status_display = ref_range.status.capitalize() if ref_range.status else "Unknown"
            
            # Map parameter names to display names
            display_names = {
                'sysBP': 'Systolic BP',
                'diaBP': 'Diastolic BP',
                'totChol': 'Total Cholesterol',
                'BMI': 'Body Mass Index',
                'glucose': 'Glucose',
                'heartRate': 'Heart Rate',
                'age': 'Age',
                'cigsPerDay': 'Cigarettes/Day',
                'gender': 'Gender',
                'currentSmoker': 'Current Smoker',
                'BPMeds': 'BP Medication',
                'prevalentStroke': 'History of Stroke',
                'prevalentHyp': 'Hypertension',
                'diabetes': 'Diabetes',
                'CP': 'Chest Pain Type'
            }
            
            parameter_display = display_names.get(param_name, param_name)
            
            result.append({
                "parameter": parameter_display,
                "value": ref_range.patient_value,
                "unit": ref_range.unit,
                "reference_range": ref_range_str,
                "status": status_display
            })
        return result

    class Config:
        from_attributes = True