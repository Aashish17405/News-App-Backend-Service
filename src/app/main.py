from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .logger import logger
from .database import engine
import sqlalchemy as sa
from .models import Base
from .routes import api_router
import logging
import subprocess
import uvicorn

# Database Initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database initialization is handled in main() before startup to ensure proper order with Alembic
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

def init_db():
    """Initialize database with extensions and tables"""
    logger.info("Initializing database...")
    with engine.begin() as conn:
        try:
            conn.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            logger.info("Extension 'uuid-ossp' verified/created.")
        except Exception as e:
            logger.error(f"Failed to create extension 'uuid-ossp': {e}")
            raise
        
        try:
            conn.execute(sa.text('CREATE EXTENSION IF NOT EXISTS vector;'))
            logger.info("Extension 'vector' verified/created.")
        except Exception as e:
            logger.warning(f"pgvector extension not available: {e}")
            logger.warning("Embeddings will use JSONB storage instead of VECTOR type.")

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully!")

def main():
    """Run the app"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Log app details
    logger.info(f"App starting in Environment: {settings.environment}")

    # Initialize DB (Extensions + Tables)
    try:
        init_db()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # We might want to continue if it's just table already exists, but critical extensions failure is bad.
        # Proceeding to alembic anyway.

    # Run Alembic migrations before starting the server
    try:
        logger.info("Checking and applying Alembic migrations...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        logger.error("Failed to apply Alembic migrations.")
        raise e

    print(f"Starting app on http://localhost:{settings.port}/... in {settings.environment} mode")
    print(f"Database URL: {settings.DATABASE_URL}")
    # Start Uvicorn server
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=settings.port, reload=True)


if __name__ == "__main__":
    main()