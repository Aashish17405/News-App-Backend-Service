from sqlalchemy import Column, String, JSON, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base

class Location(Base):
    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint('state', 'district', 'mandal_or_village', name='uq_location'),
    )
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("uuid_generate_v4()")
    )
    country = Column(String(100), nullable=False, default="India")
    state = Column(String(100), nullable=False)
    district = Column(String(100))
    mandal_or_village = Column(String(200))
    postal_code = Column(String(20))
    geo = Column(JSONB) # Stores coordinates or extra data as JSON
