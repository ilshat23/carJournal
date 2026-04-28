from typing import Sequence

from app.core.exceptions import CategoryNotFound
from app.models import Category
from app.repositories.categories import CategoryRepository


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, **kwargs):
        new_cat = await self.repo.create(**kwargs)
        return new_cat

    async def get_categories(self) -> Sequence[Category]:
        cats = await self.repo.find_all()
        return cats

    async def get_category(self, slug: str) -> Category:
        cat = await self.repo.find(slug)
        if cat is None:
            raise CategoryNotFound
        return cat
