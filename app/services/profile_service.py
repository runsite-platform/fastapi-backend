import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileUpdate


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.profile_repo = ProfileRepository(db)

    async def get_profile(self, user_id: uuid.UUID) -> Profile:
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        return profile

    async def update_profile(self, user_id: uuid.UUID, data: ProfileUpdate) -> Profile:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
            )

        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )

        updated = await self.profile_repo.update(profile.id, **update_data)
        return updated
