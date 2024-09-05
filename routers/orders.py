from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_models.orders import OrderToCreate, OrderToShow
from database_interaction import get_db
from global_constants import PaymentType
from handlers.orders import create_order_from_cart, get_order_by_id, update_order
from payments.sber import SberPaymentsService

orders_router = APIRouter()


@orders_router.post("/create/")
async def create_order(order_data: OrderToCreate, session: AsyncSession = Depends(get_db)) -> dict:
    order = await create_order_from_cart(
        user_id=order_data.user_id,
        city=order_data.city,
        street=order_data.street,
        house_number=order_data.house_number,
        apartment=order_data.apartment,
        session=session,
    )
    if order_data.payment_type == PaymentType.ONLINE:
        payment_url = SberPaymentsService(order).get_payment_url()
        await update_order(order.id, {"payment_url": payment_url}, session=session)
        return {"payment_url": payment_url, "order_id": order.id}
    return {"payment_url": "", "order_id": order.id}


@orders_router.post("/detail/{order_id}/")
async def order_detail(order_id: int, session: AsyncSession = Depends(get_db)) -> OrderToShow:
    return await get_order_by_id(order_id, session)
