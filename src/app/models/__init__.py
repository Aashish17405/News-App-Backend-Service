from .base import Base
from .user import User
from .location import Location
from .auth import OTPRequest, RefreshToken
from .role import Role, UserRole
from .reporter import ReporterProfile, ReporterVerification
from .news import News, NewsMedia, NewsModeration
from .engagement import UserEngagement, AuditLog

# Import all models here so SQLAlchemy can "see" them to create tables
__all__ = [
    "Base", 
    "User", 
    "Location", 
    "OTPRequest", 
    "RefreshToken", 
    "Role", 
    "UserRole", 
    "ReporterProfile", 
    "ReporterVerification", 
    "News", 
    "NewsMedia", 
    "NewsModeration", 
    "NewsModeration", 
    "UserEngagement", 
    "AuditLog"
]
