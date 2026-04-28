from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

from app.core.config import Settings, get_settings

settings: Settings = get_settings()

if settings.DEBUG:
    engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)
else:
    engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
