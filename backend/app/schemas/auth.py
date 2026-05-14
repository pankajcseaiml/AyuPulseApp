"""
Pydantic schemas for authentication.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    username: Optional[str] = None

from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserOut(BaseModel):
    id: PyObjectId
    name: str
    email: EmailStr
    username: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreateAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserUpdateAdmin(BaseModel):
    """Schema for admin updating user details."""
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserListResponse(BaseModel):
    """Schema for listing users (admin only)."""
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True