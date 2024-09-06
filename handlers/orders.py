from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "create_order_from_cart",
    "get_order_by_id",
    "update_order",
    "get_user_orders",
)

from api_models.orders import OrderToShow
from dals import CartDAL
from dals.orders import OrderDAL


async def create_order_from_cart(
        user_id: int,
        city: str,
        street: str,
        house_number: str,
        apartment: str,
        session: AsyncSession
) -> OrderToShow:
    async with session.begin():
        cart_dal = CartDAL(session)
        cart = await cart_dal.get_cart_by_user_id(user_id=user_id)
        if not cart.products:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Корзина пользователя пуста"
            )
        order_dal = OrderDAL(session)
        order = await order_dal.create_order(
            cart=cart,
            city=city,
            street=street,
            house_number=house_number,
            apartment=apartment
        )
    return await get_order_by_id(order.id, session=session)


async def get_order_by_id(order_id: int, session: AsyncSession) -> OrderToShow:
    async with session.begin():
        order_dal = OrderDAL(session)
        order = await order_dal.get_order_by_id(order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Заказ не найден"
            )
    return OrderToShow.model_validate(order)


async def update_order(order_id: int, update_data: dict, session: AsyncSession) -> OrderToShow:
    async with session.begin():
        order_dal = OrderDAL(session)
        order = await order_dal.update_order(order_id=order_id, update_data=update_data)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Заказ не найден"
            )
    return OrderToShow.model_validate(order)


async def get_user_orders(username: str, session: AsyncSession) -> list[OrderToShow]:
    async with session.begin():
        order_dal = OrderDAL(session)
        orders = await order_dal.get_orders_by_username(username=username)
        if not orders:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="У пользователя нет заказов"
            )
    return [OrderToShow.model_validate(order) for order in orders]
