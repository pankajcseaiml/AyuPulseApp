"""
Configuration settings for the application.
"""
import os
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "AyuPulseApp"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    
    @field_validator('DEBUG', mode='before')
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            v_lower = v.lower()
            if v_lower in ('true', '1', 'yes', 'on', 'debug'):
                return True
            if v_lower in ('false', '0', 'no', 'off', 'release'):
                return False
        # Let pydantic handle other cases (will raise validation error)
        return v
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "ayupulse"
    
    @field_validator('MONGODB_URL', mode='before')
    @classmethod
    def validate_mongodb_url(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                # If empty string, fallback to default
                return "mongodb://localhost:27017"
            # Ensure it starts with correct scheme
            if not (v.startswith("mongodb://") or v.startswith("mongodb+srv://")):
                raise ValueError("MONGODB_URL must start with 'mongodb://' or 'mongodb+srv://'")
        return v
    
    @field_validator('MONGODB_DB_NAME', mode='before')
    @classmethod
    def validate_mongodb_db_name(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return "ayupulse"
        return v
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "https://ayu-pulse-app.vercel.app",
        "https://ayupulseapp.vercel.app",
        "https://ayupulseapp-pankajcseaiml.vercel.app",
        "https://ayupulseapp.onrender.com",
        # Current Vercel deployments
        "https://frontend-kappa-lake-ahv5xllb0o.vercel.app",
        "https://frontend-hix32ikti-pankajcseaimls-projects.vercel.app",
        # Wildcard for all Vercel preview deployments
        "https://*.vercel.app"
    ]
    
    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg", ".bmp"]
    ALLOWED_ECG_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg", ".csv", ".txt"]
    
    # ML Model paths (optional)
    XRAY_MODEL_PATH: Optional[str] = os.getenv("XRAY_MODEL_PATH", "models/xray_model.pth")
    ECG_MODEL_PATH: Optional[str] = os.getenv("ECG_MODEL_PATH", "models/ecg_model.pth")
    CLINICAL_MODEL_PATH: Optional[str] = os.getenv("CLINICAL_MODEL_PATH", "models/clinical_model.pkl")
    CLINICAL_SCALER_PATH: Optional[str] = os.getenv("CLINICAL_SCALER_PATH", "ml/clinical_scaler.pkl")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()