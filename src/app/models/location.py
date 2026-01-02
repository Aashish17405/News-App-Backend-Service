from sqlalchemy import Column, String, JSON, text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Location(Base):
    __tablename__ = "locations"
    
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
    geo = Column(JSON) # Stores coordinates or extra data as JSON
