from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

# --- News Schemas ---

class NewsCreate(BaseModel):
    headline: str
    content: str
    categories: List[str]
    url: Optional[str] = None
    created_by: uuid.UUID

class NewsUpdate(BaseModel):
    headline: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[List[str]] = None
    url: Optional[str] = None

class News(BaseModel):
    id: uuid.UUID
    headline: str
    content: str
    categories: List[str]
    url: Optional[str]
    created_by: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    likes_count: int
    comments_count: int
    shares_count: int

    class Config:
        from_attributes = True

# --- News Media Schemas ---

class NewsMedia(BaseModel):
    id: uuid.UUID
    news_id: uuid.UUID
    media_type: str
    url: str
    meta_data: Optional[dict]

    class Config:
        from_attributes = True

# --- News Moderation Schemas ---

class NewsModeration(BaseModel):
    id: uuid.UUID
    news_id: uuid.UUID
    status: str
    reason: Optional[str]
    acted_by: uuid.UUID
    acted_at: datetime

    class Config:
        from_attributes = True
