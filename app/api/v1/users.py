from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.utils import handle_image_exceptions
from app.schemas import UserCreateSchema, UserResponseSchema
from app.schemas.users import RefreshTokenInputSchema, AvatarResponseSchema, \
    UserFullResponseSchema
from app.dependencies.users import current_user_dep, user_service_dep


router = APIRouter(prefix='/users', tags=['users', 'auth'])


@router.get('/', response_model=list[UserResponseSchema])
async def get_all_users(
    user_service: user_service_dep
):
    # Тестовая ручка
    response = await user_service.get_all_users()
    return response


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
)
async def register_user(
    user_service: user_service_dep,
    user_data: UserCreateSchema
):
    data = user_data.model_dump()
    data.pop('password_confirm')
    user = await user_service.register_user(**data)
    return user


@router.post(
    '/token',
    status_code=status.HTTP_201_CREATED
)
async def login(
    user_service: user_service_dep,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    tokens = await user_service.login_user(
        email=form_data.username,
        password=form_data.password
    )
    return tokens


@router.post(
    '/token/refresh',
    status_code=status.HTTP_200_OK
)
async def refresh_token(
    body: RefreshTokenInputSchema,
    user_service: user_service_dep
):
    response_data = await user_service.get_refresh_token(body.refresh_token)
    return response_data


@router.post(
    '/token/access',
    status_code=status.HTTP_200_OK
)
async def access_token(
    body: RefreshTokenInputSchema,
    user_service: user_service_dep
):
    response_data = await user_service.get_access_token(body.refresh_token)
    return response_data


@router.get(
    '/me',
    response_model=UserFullResponseSchema
)
async def get_my_profile(current_user: current_user_dep):
    return current_user


@router.put(
    '/me/avatar',
    status_code=status.HTTP_200_OK,
    response_model = AvatarResponseSchema
)
@handle_image_exceptions
async def set_avatar(
    current_user: current_user_dep,
    user_service: user_service_dep,
    file: UploadFile = File(None)
):
    """
    Загрузить аватар для текущего пользователя.

    Поддерживаемые форматы изображений: PNG, JPG/JPEG, WEBP.
    Максимальный размер: 2 MB.
    """
    await user_service.save_avatar(current_user, file) if file else None
    return current_user


@router.delete(
    '/me/avatar',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_avatar(
    current_user: current_user_dep,
    user_service: user_service_dep
):
    await user_service.remove_avatar(current_user)

