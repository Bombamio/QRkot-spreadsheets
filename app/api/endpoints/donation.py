from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity_projects import charity_projects_crud
from app.crud.donations import donations_crud
from app.services.investmant import invest
from app.models import User

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_donations_list(
    session: SessionDep,
):
    result = await donations_crud.get_multi(session)
    return result


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
):

    donation = await donations_crud.create(
        donation,
        session,
        user,
    )
    charity_project = await charity_projects_crud.get_not_fully_invested(
        session
    )

    updated_objects = invest(
        charity_project,
        donation,
    )

    session.add_all(updated_objects)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    user: Annotated[User, Depends(current_user)],
    session: SessionDep
):
    result = await donations_crud.get_by_user(user.id, session)
    return result
