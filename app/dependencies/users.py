from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError
from app.core.security import decode
from app.dependencies.db import get_db
from app.models import User
from app.repositories.users import UserRepository
from app.services.users import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepository:
    return UserRepository(db)


async def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)


user_service_dep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    user_service: user_service_dep,
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Зависимость для получения текущего пользователя, посетившего эндпоинт."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удается проверить предоставленные учетные данные',
    )
    try:
        payload = decode(token)
        user_id: int = payload.get('id')
        token_type: str = payload.get('token_type')

        if user_id is None or token_type != 'access':
            raise credentials_exception

    except (jwt.InvalidTokenError, InvalidTokenError):
        raise credentials_exception

    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise credentials_exception

    return user


current_user_dep = Annotated[User, Depends(get_current_user)]
