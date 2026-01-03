from sqlalchemy import Column, String, Text, Integer, ForeignKey, ARRAY, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import os

# Check if we should use Vector type based on environment variable
USE_PGVECTOR = os.getenv("USE_PGVECTOR", "false").lower() == "true"

if USE_PGVECTOR:
    try:
        from pgvector.sqlalchemy import Vector as VectorType
        _embedding_factory = lambda dim: VectorType(dim)
    except Exception:
        VectorType = None
        _embedding_factory = lambda dim: JSONB
else:
    # Force JSONB when pgvector extension is not available
    _embedding_factory = lambda dim: JSONB

from .base import Base

from sqlalchemy.orm import relationship

class News(Base):
    __tablename__ = "news"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    headline = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    categories = Column(ARRAY(Text), nullable=False)
    url = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(UUID(as_uuid=True))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    embedding = Column(_embedding_factory(1536), nullable=True)
    
    # Relationships
    media = relationship("NewsMedia", back_populates="news", cascade="all, delete-orphan")
    moderation = relationship("NewsModeration", back_populates="news", uselist=False, cascade="all, delete-orphan")

class NewsMedia(Base):
    __tablename__ = "news_media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String(20), nullable=False)
    url = Column(Text, nullable=False)
    metadata_ = Column('metadata', JSONB)  # maps to DB column `metadata`
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    news = relationship("News", back_populates="media")

class NewsModeration(Base):
    __tablename__ = "news_moderation"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id"), nullable=False)
    status = Column(String(30), nullable=False)
    reason = Column(Text)
    acted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    acted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    news = relationship("News", back_populates="moderation")
