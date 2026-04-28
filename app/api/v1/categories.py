from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import CategoryNotFound
from app.dependencies.categories import category_service_dep
from app.schemas.categories import CategoryCreateSchema, CategoryResponseSchema

router = APIRouter(prefix='/categories', tags=['categories'])


@router.post(
    '/',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    new_category: CategoryCreateSchema,
    service: category_service_dep
):
    category = await service.create_category(**new_category.model_dump())
    return category


@router.get(
    '/',
    response_model=list[CategoryResponseSchema]
)
async def get_categories(service: category_service_dep):
    categories = await service.get_categories()
    return categories


@router.get(
    '/{category_slug}',
    response_model=CategoryResponseSchema
)
async def get_category(service: category_service_dep, category_slug: str):
    try:
        category = await service.get_category(category_slug)
    except CategoryNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return category
