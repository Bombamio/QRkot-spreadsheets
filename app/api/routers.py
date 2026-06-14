from fastapi import APIRouter

from app.api.endpoints import (
    charity_router,
    donations_router,
    user_router,
    google_api_router,
)


main_router = APIRouter()
main_router.include_router(
    charity_router, prefix='/charity_project', tags=['Charity Projects']
)
main_router.include_router(
    donations_router, prefix='/donation', tags=['Donations']
)
main_router.include_router(
    user_router
)
main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
