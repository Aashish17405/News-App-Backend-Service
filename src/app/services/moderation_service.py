from sqlalchemy.orm import Session
from ..models.news import NewsModeration, News
from ..schemas.news import NewsModerationCreate
from datetime import datetime
import uuid

class ModerationService:
    def moderate_news(self, db: Session, news_id: uuid.UUID, mod_data: NewsModerationCreate):
        # Check if news exists
        news = db.query(News).filter(News.id == news_id).first()
        if not news:
            return None

        # Check if moderation already exists, update or create
        # Model has one-to-one (uselist=False) relation on News side?
        # Let's check DB. NewsModeration has news_id unique? 
        # The model definition didn't specify unique on news_id, but logically it might be one current status.
        # Or it could be a log.
        # My schema `News` has `moderation: Optional[NewsModeration]`. Implies single current status.
        
        existing_mod = db.query(NewsModeration).filter(NewsModeration.news_id == news_id).first()
        if existing_mod:
            existing_mod.status = mod_data.status
            existing_mod.reason = mod_data.reason
            existing_mod.acted_by = mod_data.acted_by
            existing_mod.acted_at = datetime.utcnow()
            db_mod = existing_mod
        else:
            db_mod = NewsModeration(
                news_id=news_id,
                status=mod_data.status,
                reason=mod_data.reason,
                acted_by=mod_data.acted_by
            )
            db.add(db_mod)
            
        db.commit()
        db.refresh(db_mod)
        return db_mod
