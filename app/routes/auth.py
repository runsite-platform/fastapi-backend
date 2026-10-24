from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenPair
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    service = AuthService(db)
    return await service.register(data)


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    service = AuthService(db)
    return await service.login(data)


@router.post("/refresh")
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    service = AuthService(db)
    return await service.refresh(data.refresh_token)


@router.post("/logout", status_code=204)
async def logout(_: User = Depends(get_current_user)):
    # Token invalidation requires a Redis-based blacklist in production.
    # Client must discard the token on their side.
    return Response(status_code=204)
