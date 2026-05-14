"""
MongoDB Prediction model using Beanie.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any, Annotated
from beanie import Document
from beanie.odm.fields import Indexed
from pydantic import BaseModel, Field

class ShapFeature(BaseModel):
    name: str
    display_name: str
    value: Any
    shap_value: float
    contribution_pct: float
    direction: str  # "positive" / "negative"

class ReferenceRange(BaseModel):
    normal_min: Optional[float] = None
    normal_max: Optional[float] = None
    patient_value: Any
    unit: str
    status: str  # "normal" / "borderline" / "high" / "low"

class Prediction(Document):
    user_id: Annotated[str, Indexed()]
    patient_id: Optional[Annotated[str, Indexed()]] = None
    subject_name: str
    
    # Clinical inputs (15 parameters)
    gender: int  # 0 for Female, 1 for Male
    age: int
    currentSmoker: int  # 0 or 1
    cigsPerDay: float
    BPMeds: int  # 0 or 1
    prevalentStroke: int  # 0 or 1
    prevalentHyp: int  # 0 or 1
    diabetes: int  # 0 or 1
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    heartRate: float
    glucose: float
    CP: int  # 0, 1, 2, 3
    
    # File references
    xray_original_path: Optional[str] = None
    xray_gradcam_path: Optional[str] = None
    ecg_original_path: Optional[str] = None
    ecg_gradcam_path: Optional[str] = None
    
    # ML outputs
    risk_score: float
    risk_category: str  # "Low" / "Medium" / "High"
    confidence: float
    clinical_score: float
    xray_score: Optional[float] = None
    ecg_score: Optional[float] = None
    fusion_weights: Dict[str, float]
    modalities_used: List[str]
    
    # Image analysis
    xray_analysis: Optional[str] = None
    ecg_analysis: Optional[str] = None
    
    # Explainability
    shap_features: List[ShapFeature]
    explanation_text: str
    risk_factors: List[str]
    recommendations: List[str]
    
    # Model metrics
    model_accuracy: float
    model_auc_roc: float
    model_precision: float
    model_recall: float
    model_f1: float
    
    # Reference ranges
    clinical_reference_ranges: Dict[str, ReferenceRange]
    
    # Metadata
    created_at: Annotated[datetime, Indexed()] = Field(default_factory=datetime.utcnow)
    prediction_duration_ms: int

    class Settings:
        name = "predictions"
        indexes = [
            "user_id",
            "patient_id",
            "created_at",
            "risk_category",
            # Compound indexes for common queries
            [("user_id", 1), ("created_at", -1)],
            [("patient_id", 1), ("created_at", -1)],
            [("risk_category", 1), ("created_at", -1)],
        ]