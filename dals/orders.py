from fastapi import HTTPException

from sqlalchemy import select, and_, update, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Cart, CartItem, Product, Order, OrderItem
from global_constants import PaymentStatus

__all__ = (
    "OrderDAL",
)

from settings import DELIVERY_PRICE


class OrderDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_order(
            self,
            cart: Cart,
            city: str = None,
            street: str = None,
            house_number: str = None,
            apartment: str = None
    ) -> Order:
        if city:
            total_price = cart.total_price + DELIVERY_PRICE
            delivery_price = DELIVERY_PRICE
        else:
            total_price = cart.total_price
            delivery_price = 0
        new_order = Order(
            total_price=total_price,
            delivery_price=delivery_price,
            payment_status=PaymentStatus.NOT_PAID,
            payment_url=None,
            user_id=cart.user_id,
            city=city,
            street=street,
            house_number=house_number,
            apartment=apartment
        )
        self.db_session.add(new_order)
        await self.db_session.flush()
        for product in cart.products:
            new_order_product = OrderItem(
                position_price=product.position_price,
                count=product.count,
                order_id=new_order.id,
                product_id=product.product_id
            )
            self.db_session.add(new_order_product)
        await self.db_session.flush()
        return new_order
