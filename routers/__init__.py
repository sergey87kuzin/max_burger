from fastapi import APIRouter
#
from .admin import admin_router
from .cart import cart_router
# from .stable import stable_router
from .rabbit import rabbit_router
from .orders import orders_router
from .users import user_router

main_api_router = APIRouter(prefix="/api")
# main_api_router.include_router(stable_router, prefix="/stable", tags=["stable"])
# main_api_router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
main_api_router.include_router(admin_router, prefix="/admin", tags=["Админка"])
main_api_router.include_router(cart_router, prefix="/cart", tags=["Корзина"])
main_api_router.include_router(orders_router, prefix="/orders", tags=["Заказы"])
main_api_router.include_router(rabbit_router, prefix="/rabbit", tags=["Кролик"])
main_api_router.include_router(user_router, prefix="/users", tags=["Пользователи"])
