from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# --- Role Schemas ---

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Role(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- User Role Schemas ---

class UserRoleCreate(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID
    assigned_by: Optional[uuid.UUID] = None

class UserRole(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    role_id: uuid.UUID
    assigned_by: Optional[uuid.UUID]
    assigned_at: datetime

    class Config:
        from_attributes = True
