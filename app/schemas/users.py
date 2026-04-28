from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict, \
    model_validator

from app.core.constants import UserSchemaConstants as USC


class UserCreateSchema(BaseModel):
    username: Annotated[str, Field(
        ...,
        min_length=USC.MIN_USERNAME_LEN,
        max_length=USC.MAX_USERNAME_LEN,
        pattern=USC.USERNAME_PATTERN,
        description='Имя пользователя'
    )]
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'username': 'username',
                'email': 'email@email.com',
                'password': 'myPassword',
                'password_confirm': 'myPassword'
            }
        }
    )

    @model_validator(mode='after')
    def validate(self):
        if self.password != self.password_confirm:
            raise ValueError(USC.PWD_ERR_MESSAGE)
        return self


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar_url: str | None


class UserFullResponseSchema(UserResponseSchema):
    first_name: str | None
    last_name: str | None
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

    # TODO computed_field

class AccessTokenResponseSchema(BaseModel):
    access_token: str


class RefreshTokenInputSchema(BaseModel):
    refresh_token: str


class AvatarResponseSchema(BaseModel):
    avatar_url: str | None

    model_config = ConfigDict(from_attributes=True)
