"""
Custom exceptions and exception handlers for the AyuPulseApp.
"""
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AyuPulseException(Exception):
    """Base exception for AyuPulseApp."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AyuPulseException):
    """Resource not found."""
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(message, code, status_code=404)


class UnauthorizedException(AyuPulseException):
    """Unauthorized access."""
    def __init__(self, message: str = "Unauthorized", code: str = "UNAUTHORIZED"):
        super().__init__(message, code, status_code=401)


class ForbiddenException(AyuPulseException):
    """Insufficient permissions."""
    def __init__(self, message: str = "Forbidden", code: str = "FORBIDDEN"):
        super().__init__(message, code, status_code=403)


class ValidationException(AyuPulseException):
    """Validation error."""
    def __init__(self, message: str = "Validation error", code: str = "VALIDATION_ERROR"):
        super().__init__(message, code, status_code=400)


class DatabaseException(AyuPulseException):
    """Database operation error."""
    def __init__(self, message: str = "Database error", code: str = "DATABASE_ERROR"):
        super().__init__(message, code, status_code=500)


class FileUploadException(AyuPulseException):
    """File upload error."""
    def __init__(self, message: str = "File upload error", code: str = "FILE_UPLOAD_ERROR"):
        super().__init__(message, code, status_code=400)


def setup_exception_handlers(app: FastAPI):
    """
    Register all exception handlers with the FastAPI app.
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions."""
        logger.warning(f"HTTPException {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.detail,
                "code": f"HTTP_{exc.status_code}",
                "detail": None,
                "timestamp": get_current_timestamp(),
            }
        )
    
    @app.exception_handler(AyuPulseException)
    async def ayupulse_exception_handler(request: Request, exc: AyuPulseException):
        """Handle custom AyuPulse exceptions."""
        logger.error(f"AyuPulseException: {exc.message}", exc_info=exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message,
                "code": exc.code,
                "detail": None,
                "timestamp": get_current_timestamp(),
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error.get("loc", []))
            errors.append({
                "field": field,
                "message": error.get("msg", "Invalid value"),
                "type": error.get("type"),
            })
        
        logger.warning(f"Validation error: {errors}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": "Validation failed",
                "code": "VALIDATION_ERROR",
                "detail": f"{len(errors)} validation error(s)",
                "errors": errors,
                "timestamp": get_current_timestamp(),
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal server error",
                "code": "INTERNAL_SERVER_ERROR",
                "detail": "An unexpected error occurred. Please try again later.",
                "timestamp": get_current_timestamp(),
            }
        )


def get_current_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    from datetime import datetime
    return datetime.utcnow().isoformat()