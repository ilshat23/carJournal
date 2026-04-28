from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.categories import CategoryRepository
from app.dependencies.db import get_db
from app.services.categories import CategoryService


async def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


async def get_category_service(
    repo: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repo)


category_service_dep = Annotated[CategoryService, Depends(get_category_service)]
