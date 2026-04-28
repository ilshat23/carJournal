from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.tags import get_tag_repository
from app.dependencies.vehicles import get_vehicle_repository
from app.repositories.repairs import RepairsRepository
from app.repositories.tags import TagRepository
from app.repositories.vehicles import VehicleRepository
from app.services.repairs import RepairService


async def get_repairs_repository(
    db: AsyncSession = Depends(get_db)
) -> RepairsRepository:
    return RepairsRepository(db)


async def get_repairs_service(
    repairs_repository: RepairsRepository = Depends(get_repairs_repository),
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    tag_repository: TagRepository = Depends(get_tag_repository)
) -> RepairService:
    return RepairService(
        repairs_repository,
        vehicle_repository,
        tag_repository
    )


repairs_service_dep = Annotated[RepairService, Depends(get_repairs_service)]
