from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db_models import Base, intpk, str_128, str_64, str_16, str_256

__all__ = ('User',)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str_128] = mapped_column(unique=True)
    first_name: Mapped[str_64]
    last_name: Mapped[str_64]
    phone: Mapped[str_16]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str_256]

    carts: Mapped[Optional["Cart"]] = relationship(
        back_populates='user',
        primaryjoin="User.id == Cart.user_id"
    )

    addresses: Mapped[Optional[list["Address"]]] = relationship(
        back_populates="user",
        primaryjoin="User.id == Address.user_id"
    )
    orders: Mapped[Optional[list["Order"]]] = relationship(
        back_populates="user",
        primaryjoin="User.id == Order.user_id"
    )

    def __repr__(self):
        return f"Пользователь {self.username}"
