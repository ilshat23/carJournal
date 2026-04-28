from app.core.config import get_settings


settings = get_settings()


class UserAlreadyExists(Exception):
    def __init__(self, msg: str = 'Такой пользователь уже существует.'):
        self.msg = msg
        super().__init__(self.msg)


class UserNotFoundOrInvalidCredentials(Exception):
    def __init__(self, msg: str = 'Пользователь не найден.'):
        self.msg = msg
        super().__init__(self.msg)


class InvalidTokenError(Exception):
    def __init__(self, msg: str = 'Ошибка декодирования токена'):
        self.msg = msg
        super().__init__(self.msg)


class CategoryNotFound(Exception):
    def __init__(self, msg: str = 'Категория не найдена'):
        self.msg = msg
        super().__init__(self.msg)


class TagNotFound(Exception):
    def __init__(self, msg: str = 'Тэг не найден'):
        self.msg = msg
        super().__init__(self.msg)


class VehicleNotFound(Exception):
    def __init__(self, msg: str = 'Транспорт не найден'):
        self.msg = msg
        super().__init__(self.msg)


class RepairNotFound(Exception):
    def __init__(self, msg: str = 'Ремонт не найден'):
        self.msg = msg
        super().__init__(self.msg)


class DuplicateTagsError(Exception):
    def __init__(self, msg: str = 'Теги не должны повторяться'):
        self.msg = msg
        super().__init__(self.msg)


class NotAllowedImageType(Exception):
    def __init__(
        self,
        msg: str = 'Можно загрузить изображение с расширением jpg, jpeg, png, webp'
    ):
        self.msg = msg
        super().__init__(self.msg)


class NotAllowedImageSize(Exception):
    def __init__(
        self,
        msg: str = f'Размер изображения не должен превышать {settings.MAX_IMAGE_SIZE / 1024 / 1024} МБ'
    ):
        self.msg = msg
        super().__init__(self.msg)
