from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_projects_crud
from app.crud.donations import donations_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.api.validators import (
    check_name_duplicate,
    check_charity_project_exists,
    check_full_amount_count,
    check_invested_amount_count,
    check_fully_invested,
)
from app.services.investmant import invest

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_charity_project_list(
    session: SessionDep,
):
    result = await charity_projects_crud.get_multi(session)
    return result


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    await check_name_duplicate(
        charity_project.name,
        session
    )

    charity_project = await charity_projects_crud.create(
        charity_project,
        session,
    )
    donations = await donations_crud.get_not_fully_invested(
        session
    )

    updated_objects = invest(
        donations,
        charity_project,
    )

    session.add_all(updated_objects)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
):
    charity_project = await check_charity_project_exists(
        project_id,
        session
    )

    await check_fully_invested(
        charity_project.fully_invested
    )
    if obj_in.full_amount is not None:
        await check_full_amount_count(
            obj_in.full_amount,
            charity_project.invested_amount
        )
    if obj_in.name is not None:
        await check_name_duplicate(
            obj_in.name,
            session
        )

    charity_project = await charity_projects_crud.update(
        charity_project,
        obj_in,
        session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    await check_invested_amount_count(
        charity_project.invested_amount
    )
    await check_fully_invested(
        charity_project.fully_invested
    )

    charity_project = await charity_projects_crud.remove(
        charity_project,
        session
    )
    return charity_project
