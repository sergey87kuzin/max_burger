from sqlalchemy.ext.asyncio import AsyncSession

from api_models.cart import CartToShow

__all__ = (
    "add_product_to_cart",
)

from dals import CartDAL


async def add_product_to_cart(user_id: int, product_id: int, quantity: int, session: AsyncSession) -> CartToShow:
    async with session.begin():
        cart_dal = CartDAL(session)
        cart = await cart_dal.get_cart_by_user_id(user_id=user_id)
        await cart_dal.add_product_to_cart(cart, product_id, quantity)
        result_cart = await cart_dal.get_cart_by_user_id(user_id=user_id)
    return CartToShow.model_validate(result_cart)
