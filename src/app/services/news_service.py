from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime
from ..models.news import News as NewsModel, NewsMedia
from ..schemas.news import NewsCreate, NewsUpdate, NewsFilter
import logging

logger = logging.getLogger(__name__)

class NewsService:
    # 1. Create News
    def create_news(self, db: Session, news_data: NewsCreate):
        # 1. Create News Object
        db_news = NewsModel(
            headline=news_data.headline,
            content=news_data.content,
            categories=news_data.categories,
            url=news_data.url,
            created_by=news_data.created_by
        )
        db.add(db_news)
        db.flush() # Flush to get ID for media
        
        # 2. Add Media if provided
        if news_data.media:
            for m in news_data.media:
                db_media = NewsMedia(
                    news_id=db_news.id,
                    media_type=m.media_type,
                    url=m.url,
                    metadata_=m.metadata_ # Pydantic alias handling might differ, keeping simple for now
                )
                db.add(db_media)

        db.commit()
        db.refresh(db_news)
        return db_news

    # 2. Get All News (with Filters)
    def get_all_news(self, db: Session, filter_params: NewsFilter, skip: int = 0, limit: int = 100):
        query = db.query(NewsModel).filter(NewsModel.deleted_at.is_(None))
        
        if filter_params.categories:
            # Check if ANY of the categories match (array overlap)
            # Use param binding for safety with custom op, implies array parameters
            query = query.filter(NewsModel.categories.op("&&")(filter_params.categories))
            
        if filter_params.start_date:
            query = query.filter(NewsModel.created_at >= filter_params.start_date)
            
        if filter_params.end_date:
            query = query.filter(NewsModel.created_at <= filter_params.end_date)
            
        if filter_params.search_query:
            search = f"%{filter_params.search_query}%"
            query = query.filter(
                or_(
                    NewsModel.headline.ilike(search),
                    NewsModel.content.ilike(search)
                )
            )
            
        if filter_params.created_by:
            query = query.filter(NewsModel.created_by == filter_params.created_by)

        return query.order_by(NewsModel.created_at.desc()).offset(skip).limit(limit).all()

    # 3. Get News by ID
    def get_news_by_id(self, db: Session, news_id):
        return db.query(NewsModel).filter(
            NewsModel.id == news_id,
            NewsModel.deleted_at.is_(None)
        ).first()

    # 4. Update News
    def update_news(self, db: Session, news_id, news_data: NewsUpdate):
        db_news = self.get_news_by_id(db, news_id)
        if not db_news:
            return None
            
        # Update basics
        if news_data.headline is not None:
            db_news.headline = news_data.headline
        if news_data.content is not None:
            db_news.content = news_data.content
        if news_data.categories is not None:
            db_news.categories = news_data.categories
        if news_data.url is not None:
            db_news.url = news_data.url
            
        # Update Media (Full replacement approach for simplicity, or append?)
        # For simplicity, if media is provided, we replace.
        # Ideally we'd have add_media/remove_media endpoints.
        # But here let's assume if 'media' is passed in update, we replace all.
        if news_data.media is not None:
            # Delete existing media
            db.query(NewsMedia).filter(NewsMedia.news_id == news_id).delete()
            # Add new
            for m in news_data.media:
                db_media = NewsMedia(
                    news_id=db_news.id,
                    media_type=m.media_type,
                    url=m.url,
                    metadata_=m.metadata_ 
                )
                db.add(db_media)

        db.commit()
        db.refresh(db_news)
        return db_news

    # 5. Soft Delete News
    def delete_news(self, db: Session, news_id, deleted_by_id=None):
        db_news = self.get_news_by_id(db, news_id)
        if not db_news:
            return False
            
        # Use simple manual soft delete if mixin not fully compatible or to be explicit
        db_news.deleted_at = datetime.utcnow()
        if deleted_by_id:
            db_news.deleted_by = deleted_by_id
            
        db.commit()
        return True
