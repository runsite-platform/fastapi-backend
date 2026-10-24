from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import settings


class DatabaseManager:
    engine = None
    session_maker: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def setup(cls, *, echo: bool | None = None) -> None:
        cls.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=echo if echo is not None else settings.DEBUG,
        )
        cls.session_maker = async_sessionmaker(
            bind=cls.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @classmethod
    async def stop(cls) -> None:
        if cls.engine is not None:
            await cls.engine.dispose()
            cls.engine = None
            cls.session_maker = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if DatabaseManager.session_maker is None:
        msg = "Database engine is not initialized. Call DatabaseManager.setup() first."
        raise RuntimeError(msg)

    session: AsyncSession = DatabaseManager.session_maker()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
