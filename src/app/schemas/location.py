from pydantic import BaseModel
from typing import Optional
import uuid

# When creating a location
class LocationCreate(BaseModel):
    country: str = "India"
    state: str
    district: Optional[str] = None
    mandal_or_village: Optional[str] = None
    postal_code: Optional[str] = None
    geo: Optional[dict] = None

# When updating a location
class LocationUpdate(BaseModel):
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    mandal_or_village: Optional[str] = None
    postal_code: Optional[str] = None
    geo: Optional[dict] = None

# Full location object
class Location(BaseModel):
    id: uuid.UUID
    country: str
    state: str
    district: Optional[str]
    mandal_or_village: Optional[str]
    postal_code: Optional[str]
    geo: Optional[dict]

    class Config:
        from_attributes = True
