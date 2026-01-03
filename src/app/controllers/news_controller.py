from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..services.news_service import NewsService
from ..services.moderation_service import ModerationService
from ..schemas.news import NewsCreate, NewsUpdate, NewsFilter, NewsModerationCreate
import uuid

class NewsController:
    def __init__(self):
        self.news_service = NewsService()
        self.moderation_service = ModerationService()

    # Create News Logic
    def create_news(self, db: Session, news_data: NewsCreate):
        try:
            return self.news_service.create_news(db, news_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not create news: {str(e)}"
            )

    # List News Logic
    def list_news(self, db: Session, filter_params: NewsFilter, skip: int = 0, limit: int = 100):
        return self.news_service.get_all_news(db, filter_params, skip, limit)

    # Get Single News Logic
    def get_news(self, db: Session, news_id: uuid.UUID):
        news = self.news_service.get_news_by_id(db, news_id)
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        return news

    # Update News Logic
    def update_news(self, db: Session, news_id: uuid.UUID, news_data: NewsUpdate):
        news = self.news_service.update_news(db, news_id, news_data)
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        return news

    # Delete News Logic (Soft Delete)
    def delete_news(self, db: Session, news_id: uuid.UUID, user_id: uuid.UUID = None):
        success = self.news_service.delete_news(db, news_id, deleted_by_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        return {"message": "News article deleted successfully"}

    # --- Moderation ---
    
    def moderate_news(self, db: Session, news_id: uuid.UUID, mod_data: NewsModerationCreate):
        result = self.moderation_service.moderate_news(db, news_id, mod_data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        return result
