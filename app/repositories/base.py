import uuid
from typing import Generic, TypeVar

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, entity_id: uuid.UUID) -> ModelType | None:
        return await self.db.get(self.model, entity_id)

    async def get_paginated(self, query: Select | None = None) -> Page[ModelType]:
        if query is None:
            query = select(self.model)
        return await paginate(self.db, query)

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, entity_id: uuid.UUID, **kwargs) -> ModelType | None:
        instance = await self.get_by_id(entity_id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, entity_id: uuid.UUID) -> bool:
        instance = await self.get_by_id(entity_id)
        if not instance:
            return False
        await self.db.delete(instance)
        await self.db.commit()
        return True
