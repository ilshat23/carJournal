from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Repair
from app.models.vehicles import Vehicle


class VehicleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Vehicle

    async def get(self, vehicle_id: int) -> Vehicle | None:
        vehicle = await self.db.execute(
            select(self.model)
            .filter_by(id=vehicle_id)
            .options(
                selectinload(self.model.user),
                selectinload(self.model.category),
                selectinload(self.model.repairs).selectinload(Repair.tags)
            )
        )
        return vehicle.scalar_one_or_none()

    async def create(
        self,
        name: str,
        user_id: int,
        description: str | None,
        horsepower: int | None,
        category_slug: str | None
    ):
        new_vehicle = self.model(
            name=name,
            user_id=user_id,
            description=description,
            horsepower=horsepower,
            category_slug=category_slug
        )
        self.db.add(new_vehicle)
        await self.db.commit()
        await self.db.refresh(new_vehicle)
        return new_vehicle

    async def get_all(
        self,
        page: int,
        page_size: int,
        user_id: int | None = None,
        category_slug: str | None = None
    ):
        query = select(self.model)

        if user_id:
            query.filter_by(user_id=user_id)

        if category_slug:
            query.filter_by(category_slug=category_slug)

        query = query.options(
            selectinload(self.model.user),
            selectinload(self.model.category),
        )
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return result.scalars().all()

    # async def update(
    #     self,
    #     vehicle_id: int,
    #     name: str,
    #     description: str | None,
    #     horsepower: int | None,
    #     category_slug: str | None
    # ):
    #     updated_vehicle = await self.db.execute(
    #         update(self.model).filter_by(id=vehicle_id)
    #         .values(
    #             name=name,
    #             description=description,
    #             horsepower=horsepower,
    #             category_slug=category_slug
    #         )
    #     )
    #     await self.db.commit()
    #     await self.db.refresh(updated_vehicle)
    #     return updated_vehicle

    async def update(
        self,
        vehicle: Vehicle,
        name: str,
        description: str | None,
        horsepower: int | None,
        category_slug: str | None
    ):
        vehicle.name = name

        if description is not None:
            vehicle.description = description
        if horsepower is not None:
            vehicle.horsepower = horsepower
        if category_slug is not None:
            vehicle.category_slug = category_slug

        await self.db.commit()
        await self.db.refresh(
            vehicle, attribute_names=['user', 'category', 'repairs']
        )
        return vehicle

    async def delete(self, vehicle_id: int) -> None:
        await self.db.execute(
            delete(self.model).filter_by(id=vehicle_id)
        )
        await self.db.commit()
