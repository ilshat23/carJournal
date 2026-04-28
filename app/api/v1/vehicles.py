from fastapi import APIRouter, Query, status

from app.api.v1.utils import handle_service_exceptions, vehicle_path
from app.dependencies.users import current_user_dep
from app.dependencies.vehicles import vehicle_service_dep
from app.schemas.vehicles import (
    VehCreateSchema, ShortVehResponseSchema, FullVehResponseSchema,
    VehAfterCreatingResponse, VehUpdateSchema
)


router = APIRouter(prefix='/vehicles', tags=['vehicles'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VehAfterCreatingResponse
)
@handle_service_exceptions
async def register_vehicle(
    new_data: VehCreateSchema,
    current_user: current_user_dep,
    vehicle_service: vehicle_service_dep
):
    new_vehicle = await vehicle_service.create_vehicle(
        user_id=current_user.id,
        **new_data.model_dump()
    )

    return new_vehicle


@router.get(
    '/',
    response_model=list[ShortVehResponseSchema]
)
async def get_vehicles(
    vehicle_service: vehicle_service_dep,
    category_slug: str | None = Query(None, description='Слаг категории'),
    user_id: int | None = Query(None, description='ID пользователя'),
    page: int = Query(1, ge=1, description='Номер страницы'),
    page_size: int = Query(10, ge=1, le=100, description='Размер страницы')
):
    vehicles = await vehicle_service.get_vehicles(
        category_slug=category_slug,
        user_id=user_id,
        page=page,
        page_size=page_size
    )
    return vehicles


@router.get(
    '/{vehicle_id}',
    response_model=FullVehResponseSchema
)
async def get_vehicle(
    vehicle_id: vehicle_path,
    veh_service: vehicle_service_dep
):
    vehicle = await veh_service.get_vehicle(vehicle_id)
    return vehicle


@router.patch(
    '/{vehicle_id}',
    response_model=FullVehResponseSchema,
    status_code=status.HTTP_200_OK
)
@handle_service_exceptions
async def partial_update_vehicle(
    vehicle_id: int,
    data_to_update: VehUpdateSchema,
    vehicle_service: vehicle_service_dep
):
    updated_vehicle = await vehicle_service.update_vehicle(
        vehicle_id=vehicle_id,
        **data_to_update.model_dump()
    )
    return updated_vehicle


@router.put(
    '/{vehicle_id}',
    response_model=FullVehResponseSchema,
    status_code=status.HTTP_200_OK
)
@handle_service_exceptions
async def update_vehicle(
    vehicle_id: int,
    data_to_update: VehUpdateSchema,
    vehicle_service: vehicle_service_dep
):
    updated_vehicle = await vehicle_service.update_vehicle(
        vehicle_id=vehicle_id,
        **data_to_update.model_dump()
    )
    return updated_vehicle


@router.delete(
    '/{vehicle_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
@handle_service_exceptions
async def delete_vehicle(
    vehicle_id: int,
    vehicle_service: vehicle_service_dep
):
    await vehicle_service.delete_vehicle(vehicle_id)
