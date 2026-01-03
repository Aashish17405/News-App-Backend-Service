"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings

# Get DATABASE_URL from config (which loads from .env)
db_url = settings.get("DATABASE_URL", "postgresql://postgres:aashish@localhost:5432/news_app_db")

# Create the SQLAlchemy engine
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    echo=settings.get("DATABASE_ECHO", False),
    pool_size=settings.get("DATABASE_POOL_SIZE", 5),
    max_overflow=settings.get("DATABASE_MAX_OVERFLOW", 10),
)

# SessionLocal is like your database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
