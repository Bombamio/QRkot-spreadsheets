from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDEDonation(CRUDBase):

    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        result = await session.execute(select(self.model).where(
            self.model.user_id == user_id
        ))
        return list(result.scalars().all())


donations_crud = CRUDEDonation(Donation)
