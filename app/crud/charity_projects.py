from typing import Optional

from sqlalchemy import func, select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDECharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        room_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(self.model.id).where(self.model.name == room_name)
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[CharityProject]:
        projects = await session.execute(
            select(
                self.model,
            ).where(
                self.model.fully_invested.is_(True)
            ).order_by(
                func.julianday(self.model.close_date) -
                func.julianday(self.model.create_date)
            )
        )
        return projects.scalars().all()


charity_projects_crud = CRUDECharityProject(CharityProject)
