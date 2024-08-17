from db_models import Base, intpk, str_64, str_8, str_32
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ('Address',)


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[intpk]
    name: Mapped[str_64]
    postal_code: Mapped[str_8]
    city: Mapped[str_32]
    street: Mapped[str_32]
    house_number: Mapped[str_32]
    apartment: Mapped[str_8]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='SET NULL'),
    )
    user: Mapped["User"] = relationship(
        back_populates='addresses',
        primaryjoin="User.id == Address.user_id"
    )

    def __repr__(self):
        return f"Адрес пользователя {self.user_id}"
