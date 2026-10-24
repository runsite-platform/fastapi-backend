from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, db: AsyncSession):
        super().__init__(Profile, db)

    async def get_by_user_id(self, user_id) -> Profile | None:
        query = select(Profile).where(Profile.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
