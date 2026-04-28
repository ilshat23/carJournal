from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Repair, Tag
from app.models.repairs import repairs_tags


class RepairsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Repair

    async def find(self, repair_id: int) -> Repair | None:
        repair = await self.session.execute(
            select(self.model)
            .filter_by(id=repair_id)
            .options(selectinload(self.model.tags))
        )
        return repair.scalar_one_or_none()

    async def find_all(self, vehicle_id: int) -> Sequence[Repair]:
        repairs = await self.session.execute(
            select(self.model)
            .filter_by(vehicle_id=vehicle_id)
            .options(selectinload(Repair.tags))
            .order_by(Repair.mileage.desc())
        )
        return repairs.scalars().all()

    async def create(
        self,
        description: str,
        vehicle_id: int,
        mileage: int,
        repaired_at: datetime,
        cost: Decimal,
        tag_ids: list[int] | None = None
    ):
        new_repair = self.model(
            description=description,
            vehicle_id=vehicle_id,
            repaired_at=repaired_at,
            cost=cost,
            mileage=mileage,
        )
        self.session.add(new_repair)
        await self.session.flush()

        if tag_ids:
            tags_stmt = await self.session.execute(
                select(Tag).filter(Tag.id.in_(tag_ids))
            )
            tags = tags_stmt.scalars().all()

            for tag in tags:
                await self.session.execute(
                    repairs_tags.insert().values(
                        repair_id=new_repair.id,
                        tag_id=tag.id
                    )
                )

        await self.session.commit()

        loaded_repair = await self.find(new_repair.id)

        return loaded_repair

    async def update(
        self,
        repair: Repair,
        tags: list[Tag] | None,
        description: str,
        cost: Decimal,
        mileage: int,
        repaired_at: datetime
    ):
        repair.description = description
        repair.cost = cost
        repair.mileage = mileage
        repair.repaired_at = repaired_at

        if tags is not None:
            repair.tags = tags

        await self.session.commit()
        await self.session.refresh(repair, attribute_names=['tags'])

        return repair

    async def delete(self, repair_id: int):
        await self.session.execute(
            delete(self.model).filter_by(id=repair_id)
        )
        await self.session.commit()


