from fastapi import HTTPException, status, UploadFile

from app.core.exceptions import (
    InvalidTokenError,
    UserAlreadyExists,
    UserNotFoundOrInvalidCredentials
)
from app.core.security import hash_password
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password, decode
)
from app.models import User
from app.repositories.users import UserRepository
from app.services.base import BaseService
from app.services.images import ImageService


class UserService(BaseService):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить refresh-token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.image_service = ImageService(avatar_mode=True)

    async def get_all_users(self):
        users = await self.user_repository.get_all()
        return users

    async def register_user(self, **kwargs) -> User:
        _ = await self.get_user_by_email(kwargs['email'])

        password = kwargs.pop('password')
        hashed_password = hash_password(password.get_secret_value())

        new_user = await self.user_repository.create(
            **kwargs, password=hashed_password
        )
        return new_user


    async def login_user(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise UserNotFoundOrInvalidCredentials()

        data = {
            'sub': user.email,
            'id': user.id
        }

        return {
            'access_token': create_access_token(data),
            'refresh_token': create_refresh_token(data),
            'token_type': 'bearer'
        }

    async def __get_token(
        self, refresh_token: str,
        access: bool = False
    ) -> dict:
        try:
            payload = decode(refresh_token)
            email = payload.get('sub')
            token_type = payload.get('token_type')

            if email is None or token_type != 'refresh':
                raise self.credentials_exception

        except InvalidTokenError:
            raise self.credentials_exception

        user = await self.user_repository.get_by_email(email)

        if not user:
            raise self.credentials_exception

        data = {'sub': user.email, 'id': user.id}

        token = create_access_token(data) if access else create_refresh_token(data)

        response = {
            f'{'access' if access else 'refresh'}_token': token,
            'token_type': 'bearer'
        }

        return response

    async def get_refresh_token(self, refresh_token: str) -> dict:
        res = await self.__get_token(refresh_token)
        return res


    async def get_access_token(self, refresh_token: str) -> dict:
        res = await self.__get_token(refresh_token, access=True)
        return res

    async def get_user_by_email(self, email: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)

        if existing_user:
            raise UserAlreadyExists()

        return existing_user

    async def get_user_by_id(self, idx: int) -> User | None:
        user = await self.user_repository.get_by_id(idx)
        return user

    async def save_avatar(
        self,
        current_user: User,
        new_file: UploadFile
    ):
        await self.image_service.remove_image(current_user.avatar_url)
        avatar_url = await self.image_service.save_image(new_file)
        await self.user_repository.set_avatar(current_user, avatar_url)

    async def remove_avatar(self, current_user: User):
        await self.image_service.remove_image(current_user.avatar_url)

