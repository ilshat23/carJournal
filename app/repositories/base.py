from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(
        self,
        username: str,
        email: str,
        password: str
    ):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_idx(self, idx: int):
        pass
