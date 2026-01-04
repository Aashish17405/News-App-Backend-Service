from fastapi import APIRouter
from .users import router as users_router
from .news import router as news_router
from .rbac import router as rbac_router

# Create a main router for all v1 APIs
api_router = APIRouter(prefix="/api/v1")

# Include individual routers
api_router.include_router(users_router)
api_router.include_router(news_router)
api_router.include_router(rbac_router)

__all__ = ["api_router"]
