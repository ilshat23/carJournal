from app.core.exceptions import VehicleNotFound, CategoryNotFound
from app.models import Vehicle
from app.repositories.categories import CategoryRepository
from app.repositories.vehicles import VehicleRepository


class VehiclesService:
    def __init__(
        self, vehicle_repo: VehicleRepository,
        category_repo: CategoryRepository
    ):
        self.vehicle_repo = vehicle_repo
        self.category_repo = category_repo

    async def get_vehicles(self, **kwargs):
        result = await self.vehicle_repo.get_all(**kwargs)
        return result

    async def get_vehicle(self, vehicle_id: int) -> Vehicle:
        vehicle = await self.vehicle_repo.get(vehicle_id)

        if not vehicle:
            raise VehicleNotFound

        return vehicle

    async def _check_existing_category(self, category_slug: str) -> None:
        existing_category = await self.category_repo.find(category_slug)

        if not existing_category:
            raise CategoryNotFound

    async def create_vehicle(self, **kwargs) -> Vehicle:
        await self._check_existing_category(kwargs['category_slug'])

        new_veh = await self.vehicle_repo.create(**kwargs)
        return new_veh

    async def update_vehicle(self, **kwargs) -> Vehicle:
        await self._check_existing_category(kwargs['category_slug'])
        vehicle = await self.vehicle_repo.get(kwargs.pop('vehicle_id'))

        updated_vehicle = await self.vehicle_repo.update(
            vehicle=vehicle, **kwargs
        )
        return updated_vehicle

    async def delete_vehicle(self, vehicle_id: int):
        _ = await self.vehicle_repo.get(vehicle_id)
        await self.vehicle_repo.delete(vehicle_id)
