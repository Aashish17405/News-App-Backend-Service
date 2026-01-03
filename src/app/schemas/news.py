from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

# --- News Media Schemas ---

class NewsMediaBase(BaseModel):
    media_type: str
    url: str
    metadata_: Optional[Dict[str, Any]] = None # Pydantic alias handling might be needed if mapped to 'metadata'

class NewsMediaCreate(NewsMediaBase):
    pass

class NewsMedia(NewsMediaBase):
    id: uuid.UUID
    news_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- News Moderation Schemas ---

class NewsModerationCreate(BaseModel):
    status: str
    reason: Optional[str] = None
    acted_by: uuid.UUID

class NewsModeration(NewsModerationCreate):
    id: uuid.UUID
    news_id: uuid.UUID
    acted_at: datetime

    class Config:
        from_attributes = True

# --- News Schemas ---

class NewsCreate(BaseModel):
    headline: str
    content: str
    categories: List[str]
    url: Optional[str] = None
    created_by: uuid.UUID
    media: Optional[List[NewsMediaCreate]] = None

class NewsUpdate(BaseModel):
    headline: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[List[str]] = None
    url: Optional[str] = None
    media: Optional[List[NewsMediaCreate]] = None

class NewsFilter(BaseModel):
    categories: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search_query: Optional[str] = None
    created_by: Optional[uuid.UUID] = None

class News(BaseModel):
    id: uuid.UUID
    headline: str
    content: str
    categories: List[str]
    url: Optional[str]
    created_by: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    likes_count: int
    comments_count: int
    shares_count: int
    
    media: List[NewsMedia] = []
    moderation: Optional[NewsModeration] = None

    class Config:
        from_attributes = True
