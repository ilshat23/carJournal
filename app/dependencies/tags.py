from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.repositories.tags import TagRepository
from app.services.tags import TagService


async def get_tag_repository(
    db: AsyncSession = Depends(get_db)
) -> TagRepository:
    return TagRepository(db)


async def get_tag_service(
    tag_repo: TagRepository = Depends(get_tag_repository)
) -> TagService:
    return TagService(tag_repo)


tag_service_dep = Annotated[TagService, Depends(get_tag_service)]
