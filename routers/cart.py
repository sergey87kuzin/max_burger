from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_models.cart import CartToShow, CartProductData, CartGetInfo
from database_interaction import get_db
from handlers.cart import add_product_to_cart, remove_from_cart, get_cart_list

cart_router = APIRouter()


@cart_router.post("/add/", response_model=CartToShow)
async def add_to_cart(
        add_to_cart_data: CartProductData,
        session: AsyncSession = Depends(get_db)
) -> CartToShow:
    return await add_product_to_cart(
        add_to_cart_data.user_id,
        add_to_cart_data.product_id,
        add_to_cart_data.quantity,
        session
    )


@cart_router.post("/remove/", response_model=CartToShow)
async def remove_product_from_cart(
        remove_from_cart_data: CartProductData,
        session: AsyncSession = Depends(get_db)
):
    return await remove_from_cart(
        remove_from_cart_data.user_id,
        remove_from_cart_data.product_id,
        remove_from_cart_data.quantity,
        session
    )


@cart_router.post("/list/", response_model=CartToShow)
async def cart_list(cart_data: CartGetInfo, session: AsyncSession = Depends(get_db)):
    return await get_cart_list(cart_data.user_id, session)
