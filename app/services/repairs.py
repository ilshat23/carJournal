from typing import Sequence

from app.core.exceptions import VehicleNotFound, RepairNotFound, DuplicateTagsError
from app.models import Repair
from app.repositories.repairs import RepairsRepository
from app.repositories.tags import TagRepository
from app.repositories.vehicles import VehicleRepository


class RepairService:
    def __init__(
        self,
        repair_repo: RepairsRepository,
        vehicle_repo: VehicleRepository,
        tag_repo: TagRepository
    ):
        self.repair_repo = repair_repo
        self.vehicle_repo = vehicle_repo
        self.tag_repo = tag_repo

    async def _check_existing_vehicle(self, vehicle_id: int) -> None:
        existing_vehicle = await self.vehicle_repo.get(vehicle_id)

        if not existing_vehicle:
            raise VehicleNotFound

    @staticmethod
    def _check_duplicate_tags(tag_ids: list[int]) -> None:
        unique_tag_ids = set(tag_ids)
        if len(unique_tag_ids) != len(tag_ids):
            raise DuplicateTagsError

    async def register_repair(self, **kwargs):
        await self._check_existing_vehicle(kwargs['vehicle_id'])
        new_repair = await self.repair_repo.create(**kwargs)
        return new_repair

    async def get_repair(self, repair_id: int) -> Repair:
        repair = await self.repair_repo.find(repair_id)

        if not repair:
            raise RepairNotFound

        return repair

    async def get_repairs(self, vehicle_id: int) -> Sequence[Repair]:
        await self._check_existing_vehicle(vehicle_id)
        repairs = await self.repair_repo.find_all(vehicle_id)
        return repairs

    async def update_repair(self, repair_id: int, **kwargs) -> Repair:
        tag_ids: list[int] | None = kwargs.pop('tag_ids', None)
        tags = None
        if tag_ids is not None:
            self._check_duplicate_tags(tag_ids)
            tags = await self.tag_repo.find_by_ids(tag_ids)

        repair = await self.get_repair(repair_id)
        new_repair = await self.repair_repo.update(repair, tags, **kwargs)

        return new_repair

    async def delete_repair(self, repair_id: int) -> None:
        _ = await self.get_repair(repair_id)
        await self.repair_repo.delete(repair_id)
