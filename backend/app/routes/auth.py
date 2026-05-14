"""
Authentication routes: register, login, get current user.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from app.core.security import verify_password, create_access_token, decode_access_token
from app.schemas.auth import Token, UserLogin, UserRegister, UserOut
from app.models.user import User
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await User.find_one(User.email == email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the current user has admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin role required.",
        )
    return current_user


async def get_current_staff_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the current user has staff or admin role."""
    if current_user.role not in ["staff", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Staff or admin role required.",
        )
    return current_user


async def get_current_doctor_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the current user has doctor, staff, or admin role."""
    if current_user.role not in ["doctor", "staff", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Doctor, staff, or admin role required.",
        )
    return current_user


@router.post("/register", response_model=UserOut)
async def register(user: UserRegister):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is provided and unique
    if user.username:
        existing_username = await User.find_one(User.username == user.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    from app.core.security import get_password_hash
    hashed = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        role="patient",
        hashed_password=hashed,
        is_active=True,
    )
    await new_user.insert()
    
    return UserOut(
        id=str(new_user.id),
        name=new_user.name,
        email=new_user.email,
        username=new_user.username,
        role=new_user.role,
        is_active=new_user.is_active,
        created_at=new_user.created_at,
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token for authenticated user."""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email, "user_id": str(current_user.id), "role": current_user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Force print to see if this executes
    print(f"[AUTH DEBUG] Login attempt with: {form_data.username}")
    logger.info(f"Login attempt with username: {form_data.username}")
    # Try email first
    user = await User.find_one(User.email == form_data.username)
    print(f"[AUTH DEBUG] User by email query: {user}")
    logger.info(f"User by email query: {user}")
    if not user:
        # Try username
        user = await User.find_one(User.username == form_data.username)
        print(f"[AUTH DEBUG] User by username query: {user}")
        logger.info(f"User by username query: {user}")
    if not user or not verify_password(form_data.password, user.hashed_password):
        print(f"[AUTH DEBUG] Login failed for {form_data.username}")
        logger.warning(f"Login failed for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id), "role": user.role},
        expires_delta=access_token_expires,
    )
    print(f"[AUTH DEBUG] Login successful for {user.email}")
    logger.info(f"Login successful for user {user.email} (role: {user.role})")
    # DEBUG: Return user info for testing
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        username=current_user.username,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )