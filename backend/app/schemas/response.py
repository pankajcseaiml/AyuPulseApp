"""
Generic API response schemas.
"""
from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar("T")

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    """Standard API response for successful operations."""
    success: bool = True
    message: str
    data: Optional[T] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for list endpoints."""
    success: bool = True
    message: str = "Data retrieved successfully"
    data: List[T]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ValidationErrorDetail(BaseModel):
    """Detail for validation errors."""
    field: str
    message: str
    type: Optional[str] = None

class ValidationErrorResponse(ErrorResponse):
    """Extended error response for validation errors."""
    errors: List[ValidationErrorDetail] = []

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str
    timestamp: str
    uptime: Optional[float] = None
    database: Optional[str] = None

class StatsResponse(BaseModel):
    """Statistics response."""
    success: bool = True
    message: str = "Statistics retrieved"
    data: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class FileUploadResponse(BaseModel):
    """File upload response."""
    success: bool = True
    message: str
    file_path: str
    file_name: str
    file_size: int
    content_type: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class DeleteResponse(BaseModel):
    """Delete operation response."""
    success: bool = True
    message: str
    deleted_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())