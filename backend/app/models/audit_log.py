"""
MongoDB AuditLog model using Beanie.
Tracks user activities, system events, and security logs for compliance and debugging.
"""
from datetime import datetime
from typing import Optional, Dict, Any, Annotated
from beanie import Document
from beanie.odm.fields import Indexed
from pydantic import Field
from enum import Enum


class AuditAction(str, Enum):
    """Types of audit actions"""
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"
    CREATE_PREDICTION = "create_prediction"
    VIEW_PREDICTION = "view_prediction"
    DELETE_PREDICTION = "delete_prediction"
    CREATE_PATIENT = "create_patient"
    UPDATE_PATIENT = "update_patient"
    DELETE_PATIENT = "delete_patient"
    UPDATE_PROFILE = "update_profile"
    UPLOAD_FILE = "upload_file"
    SYSTEM_EVENT = "system_event"
    ERROR = "error"
    ADMIN_ACTION = "admin_action"


class AuditLog(Document):
    """Audit log entry for tracking user and system activities"""
    # User information (if applicable)
    user_id: Optional[Annotated[str, Indexed()]] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    
    # Action details
    action: AuditAction
    resource_type: str  # "user", "prediction", "patient", "profile", "system"
    resource_id: Optional[str] = None  # ID of the affected resource
    
    # Request/response details
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None  # API endpoint
    http_method: Optional[str] = None
    status_code: Optional[int] = None
    
    # Additional data
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None  # Request duration in milliseconds
    
    # Timestamps
    created_at: Annotated[datetime, Indexed()] = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "audit_logs"
        indexes = [
            "user_id",
            "action",
            "resource_type",
            "created_at",
            # Compound index for common queries
            [("user_id", 1), ("created_at", -1)],
            [("action", 1), ("created_at", -1)],
        ]