from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Tag

    async def find(self, slug: str) -> Tag | None:
        tag = await self.db.execute(
            select(self.model).filter_by(slug=slug)
        )
        return tag.scalar_one_or_none()

    async def find_all(self) -> Sequence[Tag]:
        tags = await self.db.execute(
            select(self.model)
        )
        return tags.scalars().all()

    async def find_by_ids(self, tag_ids: list[int]) -> Sequence[Tag]:
        tags = await self.db.execute(
            select(self.model).filter(self.model.id.in_(tag_ids))
        )
        return tags.scalars().all()

    async def create(
        self,
        name: str,
        description: str | None = None
    ) -> Tag:
        tag = Tag(name=name, description=description)
        self.db.add(tag)
        await self.db.commit()
        return tag
