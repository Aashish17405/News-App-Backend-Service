from sqlalchemy import Column, String, Text, Integer, ForeignKey, ARRAY, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from .base import Base

class News(Base):
    __tablename__ = "news"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    headline = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    categories = Column(ARRAY(String), nullable=False)
    url = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(UUID(as_uuid=True))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    # Note: embedding Vector(1536) needs pgvector extension to be defined here

class NewsMedia(Base):
    __tablename__ = "news_media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String(20), nullable=False)
    url = Column(Text, nullable=False)
    meta_data = Column(JSONB) # Using meta_data to avoid reserved name conflict
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class NewsModeration(Base):
    __tablename__ = "news_moderation"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id"), nullable=False)
    status = Column(String(30), nullable=False)
    reason = Column(Text)
    acted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    acted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
