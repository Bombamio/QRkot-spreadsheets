from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser

from app.crud.charity_projects import charity_projects_crud
from app.services.google_api import (
    create_spreadsheets, update_spreadsheets_value
)

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, int]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_projects_crud.get_projects_by_completion_rate(
        session=session
    )

    spreadsheetid = await create_spreadsheets()
    await update_spreadsheets_value(
        spreadsheetid,
        projects
    )
    return projects
