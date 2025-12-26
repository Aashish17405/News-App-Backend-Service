from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from contextlib import asynccontextmanager
import time
from .config import settings
from .logger import logger
from .metrics import (
    setup_metrics,
    http_requests_total,
    http_request_duration_seconds,
    errors_total,
)


# Lifespan event handler (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events.
    
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown")
    """
    # Startup logic
    logger.info(
        "Application starting",
        extra={
            "event": "startup",
            "app_name": settings.app_name,
            "version": settings.version,
            "environment": settings.current_env,
        }
    )
    
    # You can initialize resources here (database connections, etc.)
    # Example:
    # await database.connect()
    # await redis.connect()
    
    yield  # Application is running
    
    # Shutdown logic
    logger.info(
        "Application shutting down",
        extra={
            "event": "shutdown",
            "app_name": settings.app_name,
        }
    )
    
    # Cleanup resources here
    # Example:
    # await database.disconnect()
    # await redis.disconnect()


# Create the FastAPI application with lifespan
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,  # Pass lifespan handler here
)

# Setup Prometheus metrics
setup_metrics(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for request logging and metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and record metrics"""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Incoming request",
        extra={
            "event": "request",
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
        }
    )
    
    # Process request
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        logger.error(
            "Request processing failed",
            extra={
                "event": "request_error",
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
            },
            exc_info=True,
        )
        # Record error metric
        errors_total.labels(
            error_type=type(e).__name__,
            endpoint=request.url.path
        ).inc()
        raise
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Record metrics
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    # Log response
    logger.info(
        "Request completed",
        extra={
            "event": "response",
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_seconds": round(duration, 3),
        }
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(
        "Unhandled exception",
        extra={
            "event": "unhandled_exception",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "method": request.method,
            "path": request.url.path,
        },
        exc_info=True,
    )
    
    # Record error metric
    errors_total.labels(
        error_type=type(exc).__name__,
        endpoint=request.url.path
    ).inc()
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
            "type": type(exc).__name__ if settings.debug else None,
        },
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - welcome message"""
    logger.debug("Root endpoint accessed")
    return {
        "message": "Welcome to My API!",
        "app_name": settings.app_name,
        "version": settings.version,
        "environment": settings.current_env,
    }


# Health endpoint
@app.get("/api/v1/health")
async def detailed_health():
    """Health check endpoint"""
    logger.debug("Health check endpoint accessed")
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.current_env,
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api": "ok",
            "configuration": "loaded",
        },
    }