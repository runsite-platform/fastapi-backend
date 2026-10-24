from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user


@router.patch("/me")
async def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    service = UserService(db)
    return await service.update_user(current_user.id, data)


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    await service.delete_user(current_user.id)
    return Response(status_code=204)
