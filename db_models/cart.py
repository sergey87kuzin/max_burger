from typing import Optional

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from db_models import Base, intpk, str_32

__all__ = ('Cart', "CartItem")

from global_constants import PaymentStatus


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[intpk]
    total_price: Mapped[float]
    products_count: Mapped[int]
    payment_status: Mapped[str_32] = Column(ChoiceType(PaymentStatus))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )
    user: Mapped["User"] = relationship(
        primaryjoin="User.id == Cart.user_id",
        back_populates="carts"
    )
    products: Mapped[Optional[list["CartItem"]]] = relationship(
        back_populates='cart',
        primaryjoin="Cart.id == CartItem.cart_id"
    )

    def __repr__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[intpk]
    position_price: Mapped[float]
    count: Mapped[int]
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"),
    )
    cart: Mapped["Cart"] = relationship(
        back_populates='products',
        primaryjoin="Cart.id == CartItem.cart_id"
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
    )
    product: Mapped["Product"] = relationship(
        primaryjoin="Product.id == CartItem.product_id",
    )

    def __repr__(self):
        return f"Товарная позиция в корзине {self.cart_id} товара {self.product.name}"
