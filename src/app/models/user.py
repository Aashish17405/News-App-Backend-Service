from sqlalchemy import Column, String, Boolean, UUID, text
import uuid
from .base import Base, TimestampMixin, AuditMixin, SoftDeleteMixin


class User(Base, TimestampMixin, AuditMixin, SoftDeleteMixin):

    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
        default=uuid.uuid4,
        nullable=False,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    mobile_e164 = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    preferred_language = Column(
        String(10),
        nullable=False,
        default='en'
    )
    
    role = Column(
        String(30),
        nullable=False,
        default='user',
        index=True
    )
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
        
    location_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "mobile_e164": self.mobile_e164,
            "preferred_language": self.preferred_language,
            "role": self.role,
            "is_active": self.is_active,
            "location_id": str(self.location_id) if self.location_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }