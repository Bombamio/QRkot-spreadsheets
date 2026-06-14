from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin
from app.core.constants import MAX_NAME_LENGTH


class CharityProject(CommonMixin, Base):
    """
    Модель CharityProject:

    * **`id`** - int;
    * **`name`** - str, unique;
    * **`description`** - str;
    * **`full_amount`** - int;
    * **`invested_amount`** - int;
    * **`fully_invested`** - boolean;
    * **`create_date`** - datetime;
    * **`close_date`** - datetime.
    """

    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH), unique=True, nullable=True
    )
    description: Mapped[str] = mapped_column(
        String
    )
