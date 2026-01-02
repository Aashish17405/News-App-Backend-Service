from fastapi import APIRouter
from .users import router as users_router
from .news import router as news_router

# Create a main router for all v1 APIs
api_router = APIRouter(prefix="/api/v1")

# Include individual routers
api_router.include_router(users_router)
api_router.include_router(news_router)

__all__ = ["api_router"]
