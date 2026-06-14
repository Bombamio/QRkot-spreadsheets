from typing import Optional

from pydantic import Field, field_validator

from app.schemas.base import BaseProjectModel, BaseProjectDB
from app.core.constants import (
    MAX_NAME_LENGTH, MIN_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, FULL_AMOUNT_GT
)


class CharityProjectBase(BaseProjectModel):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(
        None, min_length=MIN_DESCRIPTION_LENGTH
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: str = Field(
        ..., min_length=MIN_DESCRIPTION_LENGTH
    )
    full_amount: int = Field(..., gt=FULL_AMOUNT_GT)


class CharityProjectUpdate(CharityProjectBase):

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Название не может быть пустой строкой')
        return value


class CharityProjectDB(CharityProjectBase, BaseProjectDB):
    pass