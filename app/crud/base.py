from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        result = await session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.model_dump()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)

        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        if (
            'full_amount' in update_data and
            update_data['full_amount'] == db_obj.invested_amount
        ):
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()
