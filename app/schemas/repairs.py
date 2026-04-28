from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.tags import TagResponseSchema


class RepairBaseSchema(BaseModel):
    repaired_at: datetime | None = None
    cost: Decimal
    mileage: int
    description: str


class RepairUpdateSchema(RepairBaseSchema):
    tag_ids: list[int] | None = None


class RepairCreateSchema(RepairUpdateSchema):
    vehicle_id: int


class RepairResponseSchema(RepairBaseSchema):
    id: int
    tags: list[TagResponseSchema]

    model_config = ConfigDict(from_attributes=True)
