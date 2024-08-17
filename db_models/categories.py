from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_models import Base, intpk, str_64, str_512

__all__ = ('Category',)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str_64]
    cover: Mapped[Optional[str_512]]
    is_active: Mapped[bool] = mapped_column(default=True)

    products: Mapped[Optional[list["Product"]]] = relationship(
        back_populates="category",
        primaryjoin="Category.id == Product.category_id",
    )

    def __repr__(self) -> str:
        return f"Категория {self.name}"
