from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload, load_only
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Cart, Order, OrderItem, User
from global_constants import PaymentStatus, PaymentType

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
            payment_type: str = None,
            delivery_type: str = None,
            apartment: str = None
    ) -> Order:
        if city:
            total_price = cart.total_price + DELIVERY_PRICE
            delivery_price = DELIVERY_PRICE
        else:
            total_price = cart.total_price
            delivery_price = 0
        if not payment_type:
            payment_type = PaymentType.CASH
        new_order = Order(
            total_price=total_price,
            delivery_price=delivery_price,
            payment_status=PaymentStatus.NOT_PAID,
            payment_url=None,
            user_id=cart.user_id,
            city=city,
            street=street,
            house_number=house_number,
            payment_type=payment_type,
            delivery_type=delivery_type,
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

    async def get_order_by_id(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.products)
                .options(joinedload(OrderItem.product))
            )
            .options(
                load_only(Order.id, Order.user_id, Order.payment_status, Order.payment_url)
            )
        )
        order = await self.db_session.execute(query)
        return order.fetchone()[0]

    async def update_order(self, order_id: int, update_data: dict) -> Order:
        query = (
            update(Order)
            .where(Order.id == order_id)
            .values(**update_data)
            .returning(Order)
        )
        order = await self.db_session.execute(query)
        return order.fetchone()[0]

    async def get_orders_by_username(self, username: str) -> list[Order]:
        query = (
            select(Order)
            .join_from(Order, User)
            .options(
                selectinload(Order.products)
                .options(joinedload(OrderItem.product))
            )
            .where(User.username == username)
        )
        orders = await self.db_session.execute(query)
        orders = orders.scalars()
        return list(orders)
