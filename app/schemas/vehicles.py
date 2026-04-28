from pydantic import BaseModel, ConfigDict

from app.schemas.users import UserResponseSchema
from app.schemas.categories import CategoryResponseSchema
from app.schemas.repairs import RepairResponseSchema


class VehCommonSchema(BaseModel):
    name: str
    description: str | None
    horsepower: int | None


class VehCreateSchema(VehCommonSchema):
    category_slug: str | None


class VehUpdateSchema(VehCreateSchema):
    pass


class VehAfterCreatingResponse(VehCommonSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ShortVehResponseSchema(VehAfterCreatingResponse):
    user: UserResponseSchema


class FullVehResponseSchema(ShortVehResponseSchema):
    category: CategoryResponseSchema | None
    repairs: list[RepairResponseSchema]
