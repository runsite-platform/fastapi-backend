from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = Field("app", frozen=True)
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"

    SECRET_KEY: str = "your-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Normalize DATABASE_URL to asyncpg-compatible format."""
        if value.startswith("postgresql://") or value.startswith("postgres://"):
            value = value.replace("postgres://", "postgresql://", 1)
            value = value.replace("postgresql://", "postgresql+asyncpg://", 1)

        # asyncpg uses ?ssl=require, not ?sslmode=require
        value = value.replace("sslmode=require", "ssl=require")
        value = value.replace("sslmode=disable", "ssl=False")
        value = value.replace("sslmode=prefer", "ssl=require")

        return value


settings = Settings()
