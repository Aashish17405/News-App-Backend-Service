from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, UUID
from datetime import datetime
import uuid

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=True)

class AuditMixin:
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self, deleted_by_id: uuid.UUID = None):
        self.deleted_at = datetime.utcnow()
        if deleted_by_id:
            self.deleted_by = deleted_by_id
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
