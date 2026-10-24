from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.profiles import router as profiles_router
from app.routes.users import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(profiles_router)
