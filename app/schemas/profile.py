import uuid

from pydantic import BaseModel


class ProfileRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
