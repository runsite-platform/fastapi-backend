from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileRead, ProfileUpdate
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/users/me/profile", tags=["Profile"])


@router.get("")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProfileRead:
    service = ProfileService(db)
    return await service.get_profile(current_user.id)


@router.patch("")
async def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProfileRead:
    service = ProfileService(db)
    return await service.update_profile(current_user.id, data)
