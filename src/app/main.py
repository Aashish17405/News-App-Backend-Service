from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .logger import logger
from .database import engine
from .models import Base
from .routes import api_router

# Database Initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully!")
    yield

# Main FastAPI App
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan
)

# Security (CORS) - Allows your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all our Routes (the URL endpoints)
app.include_router(api_router)

# Welcome Message
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.version,
        "docs": "/docs" # Link to automatic API documentation
    }