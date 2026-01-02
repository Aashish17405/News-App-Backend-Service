from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# --- User Engagement Schemas ---

class UserEngagementCreate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    event_type: str
    entity_type: str
    entity_id: uuid.UUID
    meta_data: Optional[dict] = None

class UserEngagement(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    event_type: str
    entity_type: str
    entity_id: uuid.UUID
    meta_data: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Audit Log Schema ---

class AuditLog(BaseModel):
    id: uuid.UUID
    actor_id: Optional[uuid.UUID]
    actor_role: Optional[str]
    action: str
    entity_type: Optional[str]
    entity_id: Optional[uuid.UUID]
    before_state: Optional[dict]
    after_state: Optional[dict]
    ip_address: Optional[str]
    user_agent: Optional[str]
    request_id: Optional[uuid.UUID]
    created_at: datetime

    class Config:
        from_attributes = True
