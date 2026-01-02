from sqlalchemy.orm import Session
from ..models.news import News as NewsModel
from ..schemas.news import NewsCreate, NewsUpdate

class NewsService:
    # 1. Create News
    def create_news(self, db: Session, news_data: NewsCreate):
        # Convert Pydantic data into an SQLAlchemy database object
        db_news = NewsModel(
            headline=news_data.headline,
            content=news_data.content,
            categories=news_data.categories,
            url=news_data.url,
            created_by=news_data.created_by
        )
        
        # Save to database
        db.add(db_news)
        db.commit()
        db.refresh(db_news) # Get the generated ID
        
        return db_news

    # 2. Get All News
    def get_all_news(self, db: Session, skip: int = 0, limit: int = 100):
        # Fetch news list from DB, skip/limit handles "Pagination" (pages)
        return db.query(NewsModel).offset(skip).limit(limit).all()

    # 3. Get News by ID
    def get_news_by_id(self, db: Session, news_id):
        return db.query(NewsModel).filter(NewsModel.id == news_id).first()
