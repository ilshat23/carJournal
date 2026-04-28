from fastapi import APIRouter, status

from app.dependencies.tags import tag_service_dep
from app.schemas import TagCreateSchema, TagResponseSchema


router = APIRouter(prefix='/tags', tags=['tags'])


@router.post(
    '/',
    response_model=TagCreateSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_tag(
    tag_data: TagCreateSchema,
    tag_service: tag_service_dep
):
    new_tag = await tag_service.create_tag(
        name=tag_data.name,
        description=tag_data.description
    )
    return new_tag


@router.get(
    '/',
    response_model=list[TagResponseSchema]
)
async def get_tags(
    tag_service: tag_service_dep
):
    tags = await tag_service.get_tags()
    return tags
