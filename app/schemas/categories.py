from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import CategorySchemaConstants as CSC


class CategoryCreateSchema(BaseModel):
    name: Annotated[str, Field(
        ...,
        min_length=CSC.MIN_NAME_LEN,
        max_length=CSC.MAX_NAME_LEN,
        description='Наименование категории',
    )]
    description: Annotated[str | None, Field(
        description='Описание категории',
        default=None
    )]


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
