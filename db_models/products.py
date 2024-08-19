from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_models import Base, intpk, str_512, str_64, str_1024

__all__ = ('Product',)


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[intpk]
    name: Mapped[str_64]
    is_combo_product: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    price: Mapped[int]
    description: Mapped[Optional[str_1024]]
    image: Mapped[Optional[str_1024]]
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'),
    )
    category: Mapped["Category"] = relationship(
        primaryjoin="Product.category_id == Category.id",
        back_populates="products"
    )

    def __repr__(self):
        return self.name
