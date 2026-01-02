from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# --- Reporter Profile Schemas ---

class ReporterProfileCreate(BaseModel):
    user_id: uuid.UUID
    full_name: str
    reporter_code: str
    location_id: uuid.UUID
    pan_hash: Optional[str] = None
    aadhaar_hash: Optional[str] = None
    hno: Optional[str] = None
    profile_pic_url: Optional[str] = None

class ReporterProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    hno: Optional[str] = None
    profile_pic_url: Optional[str] = None
    location_id: Optional[uuid.UUID] = None

class ReporterProfile(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    reporter_code: str
    profile_pic_url: Optional[str]
    location_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Verification Schemas ---

class ReporterVerification(BaseModel):
    id: uuid.UUID
    reporter_id: uuid.UUID
    verified: bool
    trust_score: int
    verification_notes: Optional[str]
    verified_by: Optional[uuid.UUID]
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
