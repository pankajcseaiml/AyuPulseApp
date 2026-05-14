"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from app.core.config import settings
from app.routes import auth, profile, patients, predictions, health, admin
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.exceptions import setup_exception_handlers
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AyuPulseApp – Early Heart Disease Risk Prediction System",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup exception handlers
setup_exception_handlers(app)

# Custom middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# CORS - should be added last to execute first for requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

# Create upload directories on startup
def create_upload_dirs():
    """Ensure upload directories exist."""
    from app.core.config import settings
    import os
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(os.path.join(upload_dir, "xray"), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, "ecg"), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, "temp"), exist_ok=True)

# Mount static files
app.mount(f"/{settings.UPLOAD_DIR}", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Database events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    create_upload_dirs()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.api_route("/", methods=["GET", "HEAD"])
async def root(request: Request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return {"message": "Welcome to AyuPulseApp Backend API"}