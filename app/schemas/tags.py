from pydantic import BaseModel, ConfigDict


class TagCreateSchema(BaseModel):
    name: str
    description: str | None


class TagResponseSchema(TagCreateSchema):
    id: int
    slug: str

    model_config = ConfigDict(from_attributes=True)
