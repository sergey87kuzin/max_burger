from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_models import OrderToCreate
from handlers.orders import create_order_from_cart

orders_router = APIRouter()


@orders_router.post("/create/")
async def create_order(order_data: OrderToCreate, session: AsyncSession):
    return await create_order_from_cart(
        user_id=order_data.user_id,
        city=order_data.city,
        street=order_data.street,
        house_number=order_data.house_number,
        apartment=order_data.apartment,
        session=session,
    )
