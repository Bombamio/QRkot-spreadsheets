from datetime import datetime

from sqlalchemy import CheckConstraint, Integer, Boolean, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)

from app.core.config import settings


class Base(DeclarativeBase):
    pass


class CommonMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = (
        CheckConstraint(
            'full_amount >= invested_amount',
        ),
        CheckConstraint(
            'invested_amount >= 0',
        )
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    full_amount: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    close_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True
    )


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
