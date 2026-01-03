from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from ..database import get_db
from ..schemas.news import NewsCreate, NewsUpdate, News as NewsSchema, NewsFilter, NewsModerationCreate, NewsModeration
from ..controllers.news_controller import NewsController

# Create the router
router = APIRouter(prefix="/news", tags=["news"])

# Initialize the controller
controller = NewsController()

# Create News Route
@router.post("/", response_model=NewsSchema, status_code=status.HTTP_201_CREATED)
async def create_news(
    news_data: NewsCreate,
    db: Session = Depends(get_db)
):
    return controller.create_news(db, news_data)

# List All News Route (with filters)
@router.get("/", response_model=List[NewsSchema])
async def list_news(
    skip: int = 0,
    limit: int = 100,
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    search_query: Optional[str] = Query(None),
    created_by: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db)
):
    filters = NewsFilter(
        categories=categories,
        start_date=start_date,
        end_date=end_date,
        search_query=search_query,
        created_by=created_by
    )
    return controller.list_news(db, filters, skip, limit)

# Get Single News Route
@router.get("/{news_id}", response_model=NewsSchema)
async def get_news(
    news_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return controller.get_news(db, news_id)

# Update News Route
@router.put("/{news_id}", response_model=NewsSchema)
async def update_news(
    news_id: uuid.UUID,
    news_data: NewsUpdate,
    db: Session = Depends(get_db)
):
    return controller.update_news(db, news_id, news_data)

# Delete News Route
@router.delete("/{news_id}", status_code=status.HTTP_200_OK)
async def delete_news(
    news_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = Query(None, description="User performing the deletion"),
    db: Session = Depends(get_db)
):
    return controller.delete_news(db, news_id, user_id)

# --- Moderation ---

@router.post("/{news_id}/moderate", response_model=NewsModeration)
async def moderate_news(
    news_id: uuid.UUID,
    mod_data: NewsModerationCreate,
    db: Session = Depends(get_db)
):
    return controller.moderate_news(db, news_id, mod_data)
