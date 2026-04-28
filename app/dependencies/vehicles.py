from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.categories import get_category_repository
from app.repositories.categories import CategoryRepository
from app.repositories.vehicles import VehicleRepository
from app.services.vehicles import VehiclesService


async def get_vehicle_repository(
    db: AsyncSession = Depends(get_db)
) -> VehicleRepository:
    return VehicleRepository(db)


async def get_vehicle_service(
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repository),
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    return VehiclesService(vehicle_repo, category_repo)


vehicle_service_dep = Annotated[VehiclesService, Depends(get_vehicle_service)]
