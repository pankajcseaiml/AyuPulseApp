"""
MongoDB connection and database utilities using Beanie.
"""
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

# Import all Beanie Documents
from app.models.user import User
from app.models.profile import UserProfile
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.models.audit_log import AuditLog
from app.models.doctor_patient_assignments import DoctorPatientAssignment

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie."""
    # For MongoDB Atlas (mongodb+srv://) we need TLS
    if settings.MONGODB_URL.startswith("mongodb+srv://"):
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where()
        )
    else:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    await init_beanie(
        database=db.client[settings.MONGODB_DB_NAME],
        document_models=[
            User,
            UserProfile,
            Patient,
            Prediction,
            AuditLog,
            DoctorPatientAssignment,
        ],
        allow_index_dropping=True
    )
    print(f"Connected to MongoDB at {settings.MONGODB_URL}, database: {settings.MONGODB_DB_NAME} with Beanie")

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")