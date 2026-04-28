from functools import wraps
from typing import Annotated, Callable

from fastapi import HTTPException, Path, status

from app.core.exceptions import (
    CategoryNotFound,
    RepairNotFound,
    VehicleNotFound,
    DuplicateTagsError, NotAllowedImageType, NotAllowedImageSize
)


def handle_service_exceptions(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            res = await func(*args, **kwargs)
        except (
            CategoryNotFound,
            VehicleNotFound,
            RepairNotFound
        ) as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except DuplicateTagsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        return res
    return wrapper


def handle_image_exceptions(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            res = await func(*args, **kwargs)
        except (NotAllowedImageType, NotAllowedImageSize) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        return res
    return wrapper


repair_path = Annotated[int, Path(ge=0, description='ID ремонта')]
vehicle_path = Annotated[int, Path(ge=0, description='ID транспорта')]
