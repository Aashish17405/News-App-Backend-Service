from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# What we need when creating a new user
class UserCreate(BaseModel):
    username: str
    mobile_e164: str
    preferred_language: str = "en"
    role: str = "user"
    location_id: Optional[uuid.UUID] = None

# What we need when updating a user (everything is optional)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    mobile_e164: Optional[str] = None
    preferred_language: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    location_id: Optional[uuid.UUID] = None

# What a User looks like when we get it from the database
class User(BaseModel):
    id: uuid.UUID
    username: str
    mobile_e164: str
    preferred_language: str
    role: str
    is_active: bool
    location_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
