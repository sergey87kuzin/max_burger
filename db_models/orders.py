from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from db_models import Base, intpk, str_32, str_128, str_64, str_16

__all__ = ("Order", "OrderItem")

from global_constants import PaymentStatus, PaymentType, DeliveryType


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    created_at: Mapped[Optional[datetime]]
    total_price: Mapped[float]
    delivery_price: Mapped[int]
    delivery_type: Mapped[str_32] = Column(ChoiceType(DeliveryType))
    payment_status: Mapped[str_32] = Column(ChoiceType(PaymentStatus))
    payment_url: Mapped[Optional[str_128]]
    payment_type: Mapped[str_16] = Column(ChoiceType(PaymentType))
    city: Mapped[Optional[str_64]]
    street: Mapped[Optional[str_64]]
    house_number: Mapped[Optional[str_64]]
    apartment: Mapped[Optional[str_64]]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user: Mapped["User"] = relationship(
        primaryjoin="User.id == Order.user_id",
        back_populates="orders"
    )
    products: Mapped[list["OrderItem"]] = relationship(
        back_populates='order',
        primaryjoin="Order.id == OrderItem.order_id"
    )

    def __repr__(self):
        return f"Заказ пользователя {self.user.username}"


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[intpk]
    position_price: Mapped[float]
    count: Mapped[int]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
    )
    order: Mapped["Order"] = relationship(
        back_populates='products',
        primaryjoin="Order.id == OrderItem.order_id"
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
    )
    product: Mapped["Product"] = relationship(
        primaryjoin="Product.id == OrderItem.product_id",
    )

    def __repr__(self):
        return f"Товарная позиция в заказе {self.order_id} товара {self.product.name}"
