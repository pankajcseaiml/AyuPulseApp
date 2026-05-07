from fastapi import APIRouter, Depends, HTTPException, status
from app.models.profile import UserProfile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from app.routes.auth import get_current_user
from app.schemas.response import StandardResponse
from datetime import datetime

router = APIRouter()

@router.post("", response_model=StandardResponse[ProfileOut])
async def create_profile(profile_data: ProfileCreate, current_user: User = Depends(get_current_user)):
    existing = await UserProfile.find_one(UserProfile.user_id == str(current_user.id))
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
        
    # Auto calculate age if needed (though passed in schema)
    today = datetime.today().date()
    dob = profile_data.date_of_birth
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    new_profile = UserProfile(
        user_id=str(current_user.id),
        age=age,
        **profile_data.model_dump()
    )
    await new_profile.insert()
    
    return StandardResponse(
        success=True,
        message="Profile created successfully",
        data=ProfileOut(**new_profile.model_dump())
    )

@router.get("", response_model=StandardResponse[ProfileOut])
async def get_profile(current_user: User = Depends(get_current_user)):
    profile = await UserProfile.find_one(UserProfile.user_id == str(current_user.id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    return StandardResponse(
        success=True,
        message="Profile retrieved",
        data=ProfileOut(**profile.model_dump())
    )

@router.put("", response_model=StandardResponse[ProfileOut])
async def update_profile(profile_update: ProfileUpdate, current_user: User = Depends(get_current_user)):
    profile = await UserProfile.find_one(UserProfile.user_id == str(current_user.id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    update_data = profile_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    # Recalculate age if DOB changed
    if "date_of_birth" in update_data:
        today = datetime.today().date()
        dob = profile.date_of_birth
        profile.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
    profile.updated_at = datetime.utcnow()
    await profile.save()
    
    return StandardResponse(
        success=True,
        message="Profile updated successfully",
        data=ProfileOut(**profile.model_dump())
    )
