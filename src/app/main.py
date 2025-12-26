from fastapi import FastAPI
from datetime import datetime
from .config import settings

# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
)

# Root endpoint - just says hello
@app.get("/")
async def root():
    return {
        "message": "Welcome to News App Backend!",
        "app_name": settings.app_name,
        "version": settings.version,
        "environment": settings.current_env,
    }


# health endpoint (detailed version)
@app.get("/api/v1/health")
async def detailed_health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.current_env,
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api": "ok",
            "configuration": "loaded",
        }
    }