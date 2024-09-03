from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "create_order_from_cart",
)

from api_models import OrderToShow
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
    return OrderToShow.model_validate(order)
