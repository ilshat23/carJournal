from typing import Any, Coroutine, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Category

    async def find(self, slug: str) -> Category | None:
        cat = await self.db.execute(
            select(self.model).filter_by(slug=slug)
        )
        return cat.scalar_one_or_none()

    async def find_all(self) -> Sequence[Category]:
        cats = await self.db.execute(
            select(self.model)
        )
        return cats.scalars().all()

    async def create(
        self,
        name: str,
        description: str | None
    ) -> Category:
        new_cat = self.model(
            name=name,
            description=description
        )
        self.db.add(new_cat)
        await self.db.commit()
        return new_cat
