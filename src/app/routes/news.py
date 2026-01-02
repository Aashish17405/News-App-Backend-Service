from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db
from ..schemas.news import NewsCreate, News as NewsSchema
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

# List All News Route
@router.get("/", response_model=List[NewsSchema])
async def list_news(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return controller.list_news(db, skip, limit)

# Get Single News Route
@router.get("/{news_id}", response_model=NewsSchema)
async def get_news(
    news_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return controller.get_news(db, news_id)
