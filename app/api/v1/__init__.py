from fastapi import APIRouter

from app.api.v1.categories import router as categories_router
from app.api.v1.repairs import router as repairs_router
from app.api.v1.tags import router as tags_router
from app.api.v1.users import router as users_router
from app.api.v1.vehicles import router as vehicles_router


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(users_router)
v1_router.include_router(categories_router)
v1_router.include_router(tags_router)
v1_router.include_router(vehicles_router)
v1_router.include_router(repairs_router)
