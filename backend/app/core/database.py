"""
MongoDB connection and database utilities using Beanie.
"""
import certifi
import re
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import InvalidURI
from app.core.config import settings

def mask_mongodb_url(url: str) -> str:
    """
    Mask password in MongoDB URL for safe logging.
    Replaces 'mongodb://username:password@host' with 'mongodb://username:*****@host'
    and 'mongodb+srv://username:password@host' similarly.
    """
    if not isinstance(url, str):
        return str(url)
    # Pattern to match credentials
    pattern = r'(mongodb(?:\+srv)?://)([^:]+):([^@]+)@'
    def replace(match):
        scheme = match.group(1)
        username = match.group(2)
        # password = match.group(3)  # not used
        return f"{scheme}{username}:*****@"
    try:
        masked = re.sub(pattern, replace, url, count=1)
        return masked
    except Exception:
        # If anything goes wrong, return a safe version
        if '://' in url:
            # Keep scheme, mask everything after @?
            parts = url.split('@', 1)
            if len(parts) == 2:
                return parts[0].split('://')[0] + '://*****@' + parts[1]
        return 'mongodb://*****'

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
    masked_url = mask_mongodb_url(settings.MONGODB_URL)
    print(f"Attempting to connect to MongoDB at {masked_url}, database: {settings.MONGODB_DB_NAME}")
    
    try:
        # For MongoDB Atlas (mongodb+srv://) we need TLS
        if settings.MONGODB_URL.startswith("mongodb+srv://"):
            db.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                tls=True,
                tlsCAFile=certifi.where()
            )
        else:
            db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    except InvalidURI as e:
        raise ValueError(
            f"Invalid MongoDB connection string. "
            f"URL must start with 'mongodb://' or 'mongodb+srv://'. "
            f"Current URL (masked): {masked_url}. "
            f"Original error: {e}"
        ) from e
    except Exception as e:
        raise ConnectionError(
            f"Failed to connect to MongoDB at {masked_url}. "
            f"Check network, credentials, and firewall settings. "
            f"Error: {e}"
        ) from e
    
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
    print(f"Connected to MongoDB at {masked_url}, database: {settings.MONGODB_DB_NAME} with Beanie")

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")