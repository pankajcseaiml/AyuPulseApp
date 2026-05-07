"""
Health check endpoints.
"""
from fastapi import APIRouter
from datetime import datetime
import time

from app.schemas.response import HealthResponse
from app.models.user import User
from app.core.config import settings

router = APIRouter()

# Track startup time for uptime calculation
_start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.
    """
    uptime = time.time() - _start_time
    
    # Check database connectivity
    db_status = "unknown"
    try:
        # Try to ping the database
        await User.find().limit(1).count()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)[:50]}"
    
    return HealthResponse(
        status="healthy",
        service="AyuPulseApp Backend",
        version=settings.VERSION,
        timestamp=datetime.utcnow().isoformat(),
        uptime=round(uptime, 2),
        database=db_status,
    )

@router.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": datetime.utcnow().isoformat()}

@router.get("/info")
async def service_info():
    """
    Service information endpoint.
    """
    return {
        "service": "AyuPulseApp Backend",
        "version": settings.VERSION,
        "description": "Early Heart Disease Risk Prediction System",
        "environment": getattr(settings, "ENVIRONMENT", "development"),
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "timestamp": datetime.utcnow().isoformat(),
    }