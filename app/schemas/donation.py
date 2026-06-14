from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from app.schemas.base import BaseProjectModel


class DonationBase(BaseProjectModel):
    comment: Optional[str] = Field(None, min_length=1)


class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)


class DonationDB(DonationBase):
    id: int
    full_amount: int = Field(..., gt=0)
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: Optional[int] = None
