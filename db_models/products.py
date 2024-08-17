from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_models import Base, intpk, str_512, str_64

__all__ = ('Product', "ProductImage")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[intpk]
    name: Mapped[str_64]
    is_combo_product: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    price: Mapped[int]
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'),
    )
    category: Mapped["Category"] = relationship(
        primaryjoin="Product.category_id == Category.id",
        back_populates="products"
    )
    images: Mapped[Optional[list["ProductImage"]]] = relationship(
        back_populates="product",
        primaryjoin="Product.id == ProductImage.product_id",
    )

    def __repr__(self):
        return self.name


class ProductImage(Base):
    __tablename__ = 'product_images'

    id: Mapped[intpk]
    cart_image: Mapped[str_512]
    catalog_image: Mapped[str_512]
    order: Mapped[int]
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete='CASCADE'),
    )
    product: Mapped["Product"] = relationship(
        back_populates='images',
        primaryjoin="Product.id == ProductImage.product_id"
    )

    def __repr__(self):
        return f"Картинка номер {self.order} товара {self.product_id}"
