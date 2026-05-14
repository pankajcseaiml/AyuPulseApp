from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.auth import UserOut, UserUpdateAdmin, UserCreateAdmin
from app.routes.auth import get_current_admin, get_current_staff_or_admin
from app.schemas.response import StandardResponse
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/users", response_model=StandardResponse[UserOut])
async def create_user(user_data: UserCreateAdmin, current_admin: User = Depends(get_current_admin)):
    # Check if exists
    existing = await User.find_one(User.email == user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Valid roles
    if user_data.role not in ["patient", "doctor", "staff", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True
    )
    await new_user.insert()
    
    return StandardResponse(
        success=True,
        message="User created by admin",
        data=UserOut(
            id=str(new_user.id),
            name=new_user.name,
            email=new_user.email,
            username=new_user.username,
            role=new_user.role,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
    )


@router.get("/users", response_model=StandardResponse[List[UserOut]])
async def list_users(current_admin: User = Depends(get_current_staff_or_admin)):
    users = await User.find_all().to_list()
    data = [UserOut(
        id=str(u.id), name=u.name, email=u.email, username=u.username, role=u.role, is_active=u.is_active, created_at=u.created_at
    ) for u in users]
    return StandardResponse(success=True, message="Users retrieved", data=data)

@router.get("/users/{user_id}", response_model=StandardResponse[UserOut])
async def get_user(user_id: str, current_admin: User = Depends(get_current_staff_or_admin)):
    try:
        user = await User.get(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return StandardResponse(
        success=True,
        message="User retrieved",
        data=UserOut(id=str(user.id), name=user.name, email=user.email, username=user.username, role=user.role, is_active=user.is_active, created_at=user.created_at)
    )

@router.put("/users/{user_id}", response_model=StandardResponse[UserOut])
async def update_user(user_id: str, update_data: UserUpdateAdmin, current_admin: User = Depends(get_current_admin)):
    try:
        user = await User.get(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)
    
    user.updated_at = datetime.utcnow()
    await user.save()
    
    return StandardResponse(
        success=True,
        message="User updated",
        data=UserOut(id=str(user.id), name=user.name, email=user.email, username=user.username, role=user.role, is_active=user.is_active, created_at=user.created_at)
    )

@router.delete("/users/{user_id}", response_model=StandardResponse[None])
async def delete_user(user_id: str, current_admin: User = Depends(get_current_admin)):
    if user_id == str(current_admin.id):
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account")
        
    try:
        user = await User.get(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    await user.delete()
    return StandardResponse(success=True, message="User deleted", data=None)

@router.post("/users/{user_id}/toggle-active", response_model=StandardResponse[UserOut])
async def toggle_active(user_id: str, current_admin: User = Depends(get_current_admin)):
    if user_id == str(current_admin.id):
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
        
    try:
        user = await User.get(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_active = not user.is_active
    user.updated_at = datetime.utcnow()
    await user.save()
    
    return StandardResponse(
        success=True,
        message=f"User {'activated' if user.is_active else 'deactivated'}",
        data=UserOut(id=str(user.id), name=user.name, email=user.email, username=user.username, role=user.role, is_active=user.is_active, created_at=user.created_at)
    )

@router.get("/stats", response_model=StandardResponse[dict])
async def system_stats(current_admin: User = Depends(get_current_staff_or_admin)):
    total_users = await User.count()
    total_predictions = await Prediction.count()
    
    from datetime import datetime, time
    today_start = datetime.combine(datetime.utcnow().date(), time.min)
    
    predictions_today = await Prediction.find(Prediction.created_at >= today_start).count()
    
    all_predictions = await Prediction.find_all().to_list()
    avg_risk = sum(p.risk_score for p in all_predictions) / max(1, total_predictions)
    
    risk_distribution = {
        "Low": sum(1 for p in all_predictions if p.risk_category == "Low"),
        "Medium": sum(1 for p in all_predictions if p.risk_category == "Medium"),
        "High": sum(1 for p in all_predictions if p.risk_category == "High")
    }
    
    # Very simple aggregation for charts (last 7 days could be better, but this works)
    
    return StandardResponse(
        success=True,
        message="System stats retrieved",
        data={
            "total_users": total_users,
            "total_predictions": total_predictions,
            "predictions_today": predictions_today,
            "average_risk_score": float(avg_risk),
            "risk_distribution": risk_distribution
        }
    )