from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository(object):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.model = User

    async def create(self, username: str, email: str, password: str) -> User:
        user = self.model(
            username=username,
            email=email,
            hashed_password=password
        )
        self.db.add(user)
        await self.db.commit()
        return user


    async def get_by_email(self, email: str ) -> User | None:
        user = await self.db.execute(
            select(self.model).filter_by(email=email)
        )
        return user.scalar_one_or_none()

    async def get_by_id(self, idx: int) -> User | None:
        user = await self.db.execute(
            select(self.model).filter_by(id=idx)
        )
        return user.scalar_one_or_none()

    async def get_all(self):
        users = await self.db.execute(
            select(self.model)
        )
        return users.scalars().all()

    async def set_avatar(self, user: User, url: str):
        user.avatar_url = url
        await self.db.commit()