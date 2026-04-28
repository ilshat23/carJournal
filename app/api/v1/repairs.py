from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.v1.utils import (
    handle_service_exceptions,
    repair_path,
    vehicle_path
)
from app.dependencies.repairs import repairs_service_dep
from app.schemas import RepairResponseSchema, RepairCreateSchema
from app.schemas.repairs import RepairUpdateSchema


router = APIRouter(prefix='/repairs', tags=['repairs'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RepairResponseSchema
)
@handle_service_exceptions
async def register_repair(
    new_data: RepairCreateSchema,
    repair_service: repairs_service_dep,
):
    repair = await repair_service.register_repair(**new_data.model_dump())
    return repair


@router.get(
    '/',
    response_model=list[RepairResponseSchema]
)
@handle_service_exceptions
async def get_repairs(
    repair_service: repairs_service_dep,
    vehicle_id: Annotated[int, Query(ge=0, description='ID транспорта')]
):
    repairs = await repair_service.get_repairs(vehicle_id)
    return repairs


@router.get('/{repair_id}', response_model=RepairResponseSchema)
@handle_service_exceptions
async def get_repair(
    repair_service: repairs_service_dep,
    repair_id: repair_path
):
    repair = await repair_service.get_repair(repair_id)
    return repair


@router.put(
    '/{repair_id}',
    response_model=RepairResponseSchema,
    status_code=status.HTTP_200_OK
)
@handle_service_exceptions
async def update_repair(
    repair_service: repairs_service_dep,
    data_to_update: RepairUpdateSchema,
    repair_id: repair_path
):
    updated_repair = await repair_service.update_repair(
        repair_id,
        **data_to_update.model_dump()
    )
    return updated_repair


@router.patch(
    '/{repair_id}',
    response_model=RepairResponseSchema,
    status_code=status.HTTP_200_OK
)
@handle_service_exceptions
async def partial_update_repair(
    repair_service: repairs_service_dep,
    data_to_update: RepairUpdateSchema,
    repair_id: repair_path
):
    updated_repair = await repair_service.update_repair(
        repair_id,
        **data_to_update.model_dump()
    )
    return updated_repair


@router.delete(
    '/{repair_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_repair(
    repair_service: repairs_service_dep,
    repair_id: repair_path
):
    await repair_service.delete_repair(repair_id)
