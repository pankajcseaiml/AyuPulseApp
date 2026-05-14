"""
MongoDB User model using Beanie.
"""
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    name: str
    email: EmailStr
    username: Optional[str] = None
    role: str = "patient"  # patient, doctor, staff, admin
    is_active: bool = True
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            "email",
            "username",
            "role",
            "is_active",
        ]