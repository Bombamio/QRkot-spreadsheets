from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_projects import charity_projects_crud
from app.core.google_client import get_service
from app.models import CharityProject
from app.services.google_api import (
    create_spreadsheets_oauth, update_spreadsheets_value_oauth,
    create_spreadsheets, set_user_permissions, update_spreadsheets_value
)

router = APIRouter()


# OAuth 2.0
@router.post(
    '/oauth',
    response_model=list[CharityProject],
    dependencies=[Depends(current_superuser)],
)
async def get_report_oauth(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_projects_crud.get_projects_by_completion_rate(
        session=session
    )

    spreadsheetid = await create_spreadsheets_oauth()
    await update_spreadsheets_value_oauth(
        spreadsheetid,
        projects
    )
    return projects


# Service Account
@router.post(
    '/',
    response_model=list[CharityProject],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_projects_crud.get_projects_by_completion_rate(
        session=session
    )
    spreadsheetid = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await update_spreadsheets_value(
        spreadsheetid,
        projects,
        wrapper_services
    )
    return projects
