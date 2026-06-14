from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BaseProjectModel(BaseModel):
    __abstract__ = True

    full_amount: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(
        extra="forbid",
    )


class BaseProjectDB(BaseProjectModel):
    __abstract__ = True

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
