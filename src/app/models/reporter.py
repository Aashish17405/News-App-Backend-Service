from sqlalchemy import Column, String, CHAR, Boolean, Integer, Text, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .base import Base

class ReporterProfile(Base):
    __tablename__ = "reporter_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    reporter_code = Column(CHAR(5), unique=True, nullable=False)
    pan_hash = Column(String(256))
    aadhaar_hash = Column(String(256))
    hno = Column(String(128))
    profile_pic_url = Column(Text)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)

class ReporterVerification(Base):
    __tablename__ = "reporter_verification"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("reporter_profiles.id"), unique=True, nullable=False)
    verified = Column(Boolean, default=False)
    trust_score = Column(Integer, default=0)
    verification_notes = Column(Text)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
