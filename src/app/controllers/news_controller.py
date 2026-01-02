from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..services.news_service import NewsService
from ..schemas.news import NewsCreate

class NewsController:
    def __init__(self):
        self.service = NewsService()

    # Create News Logic
    def create_news(self, db: Session, news_data: NewsCreate):
        try:
            return self.service.create_news(db, news_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not create news: {str(e)}"
            )

    # List News Logic
    def list_news(self, db: Session, skip: int = 0, limit: int = 100):
        # We can add extra filters here later (like category)
        return self.service.get_all_news(db, skip, limit)

    # Get Single News Logic
    def get_news(self, db: Session, news_id):
        news = self.service.get_news_by_id(db, news_id)
        if not news:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        return news
