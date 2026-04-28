import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.exceptions import NotAllowedImageType, NotAllowedImageSize


settings = get_settings()


class ImageService:
    def __init__(self, avatar_mode: bool = False):
        self.allowed_types: set[str] = settings.ALLOWED_IMAGE_TYPES
        self.max_size: int = settings.MAX_IMAGE_SIZE
        self.avatar_mode: bool = avatar_mode

        if self.avatar_mode:
            self.images_dir = settings.MEDIA_AVATARS
            self.default_image = settings.DEFAULT_AVATAR_IMAGE
        else:
            self.images_dir = settings.MEDIA_VEHICLES
            self.default_image = settings.DEFAULT_VEHICLE_IMAGE

        self.images_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, file: UploadFile) -> str:
        """
        Сохраняет изображение.

        Выполняет базовую валидацию и возвращает относительный url.
        """
        if file.content_type not in self.allowed_types:
            raise NotAllowedImageType

        content = await file.read()

        if len(content) > self.max_size:
            raise NotAllowedImageSize

        extension = Path(file.filename or '').suffix.lower() or '.jpg'
        filename = f'{uuid.uuid4()}{extension}'

        if self.avatar_mode:
            filepath = self.images_dir / filename
            rel_path = f'media/avatars/{filename}'
        else:
            filepath = self.images_dir / filename
            rel_path = f'media/vehicles/{filename}'

        filepath.write_bytes(content)

        return rel_path

    @staticmethod
    async def remove_image(url: str | None) -> None:
        if not url:
            return

        rel_path = url.lstrip('/')
        file_path = settings.BASE_DIR / rel_path

        if file_path.exists():
            file_path.unlink()

    def get_image(self, url: str | None) -> str:
        if not url:
            return self.default_image

        return url
