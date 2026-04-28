from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///./car_journal.db'
    APP_NAME: str = 'car_journal'
    SECRET_KEY: str = ''
    ALGORITHM: str = ''
    DEBUG: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    # media
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    MEDIA_ROOT: Path = BASE_DIR / 'media'
    MEDIA_AVATARS: Path = MEDIA_ROOT / 'avatars'
    MEDIA_VEHICLES: Path = MEDIA_AVATARS / 'vehicles'
    MAX_IMAGE_SIZE: int = 2 * 1024 * 1024
    ALLOWED_IMAGE_TYPES: set[str] = {'image/jpeg', 'image/png', 'image/webp', 'image/jpg'}

    DEFAULT_AVATAR_IMAGE: str = 'media/avatars/default.jpg'
    DEFAULT_VEHICLE_IMAGE: str = 'media/vehicles/default.jpg'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
