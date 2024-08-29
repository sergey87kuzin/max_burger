from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_models.cart import CartToShow, AddToCart
from database_interaction import get_db
from handlers.cart import add_product_to_cart

cart_router = APIRouter()


@cart_router.post("/add/")
async def add_to_cart(
        add_to_cart_data: AddToCart,
        session: AsyncSession = Depends(get_db)
) -> CartToShow:
    return await add_product_to_cart(
        add_to_cart_data.user_id,
        add_to_cart_data.product_id,
        add_to_cart_data.quantity,
        session
    )
