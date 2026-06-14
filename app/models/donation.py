from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class Donation(CommonMixin, Base):
    """
    Модель Donation:

    * **`id`** - int;
    * **`comment`** - str;
    * **`full_amount`** - int;
    * **`invested_amount`** - int;
    * **`fully_invested`** - boolean;
    * **`create_date`** - datetime;
    * **`close_date`** - datetime.
    """

    comment: Mapped[str] = mapped_column(
        String, nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_reservation_user_id_user'),
        nullable=True
    )
