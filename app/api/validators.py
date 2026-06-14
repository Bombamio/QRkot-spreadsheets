from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_projects_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_projects_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_full_amount_count(
        new_full_amount: int,
        old_full_amount: int,
) -> None:
    if new_full_amount < old_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нелья установить значение full_amount меньше уже '
                'вложенной суммы.'
            ),
        )


async def check_invested_amount_count(
        invested_amount: int
) -> None:
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_fully_invested(
        fully_invested: bool
) -> None:
    if fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалять закрытый проект!'
        )


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,

) -> None:
    room_id = await charity_projects_crud.get_project_id_by_name(
        project_name, session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )
