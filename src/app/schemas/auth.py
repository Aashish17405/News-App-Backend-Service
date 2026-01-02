from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# --- OTP Request Schemas ---

class OTPRequestCreate(BaseModel):
    mobile_e164: str
    purpose: str

class OTPRequest(BaseModel):
    id: uuid.UUID
    mobile_e164: str
    purpose: str
    issued_at: datetime
    expires_at: datetime
    used: bool

    class Config:
        from_attributes = True

# --- Refresh Token Schemas ---

class RefreshTokenCreate(BaseModel):
    user_id: uuid.UUID
    token_hash: str
    expires_at: datetime

class RefreshToken(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    issued_at: datetime
    expires_at: datetime
    revoked: bool

    class Config:
        from_attributes = True
