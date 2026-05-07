"""
Custom middleware for the AyuPulseApp.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        # Log request
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        method = request.method
        url = request.url.path
        query_params = str(request.query_params) if request.query_params else ""
        
        logger.info(f"Request: {method} {url}?{query_params} from {client_host}")
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request {method} {url}: {str(e)}")
            raise
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        status_code = response.status_code
        logger.info(
            f"Response: {method} {url} -> {status_code} "
            f"(took {process_time:.3f}s)"
        )
        
        # Add header with processing time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to responses."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # For APIs, we don't need CSP but we can add it if needed
        # response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response