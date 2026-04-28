from typing import Sequence

from app.core.exceptions import TagNotFound
from app.models import Tag
from app.repositories.tags import TagRepository


class TagService:
    def __init__(self, repo: TagRepository):
        self.repo = repo

    async def get_tag(self, slug: str) -> Tag:
        tag = await self.repo.find(slug)
        if not tag:
            raise TagNotFound
        return tag

    async def create_tag(self, **kwargs):
        tag = await self.repo.create(**kwargs)
        return tag

    async def get_tags(self) -> Sequence[Tag]:
        tags = await self.repo.find_all()
        return tags
