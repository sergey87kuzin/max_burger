from fastapi import HTTPException

from sqlalchemy import select, and_, update, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Cart, CartItem, Product
from global_constants import PaymentStatus

__all__ = (
    "CartDAL",
)


class CartDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        cart_query = (
            select(Cart)
            .where(and_(
                Cart.user_id == user_id,
                Cart.payment_status == PaymentStatus.NOT_PAID
            ))
            .options(
                selectinload(Cart.products)
                .options(
                    joinedload(CartItem.product, innerjoin=True),
                )
            )
        )
        cart = await self.db_session.execute(cart_query)
        cart = cart.fetchone()
        if cart:
            return cart[0]
        new_cart = Cart(
            user_id=user_id,
            products_count=0,
            total_price=0,
            payment_status=PaymentStatus.NOT_PAID
        )
        self.db_session.add(new_cart)
        await self.db_session.flush()
        return new_cart

    async def add_product_to_cart(self, cart: Cart, product_id: int, quantity: int) -> None:
        product_query = select(Product).where(Product.id == product_id)
        product_row = await self.db_session.execute(product_query)
        product = product_row.fetchone()[0]
        if cart.products_count == 0:
            items = []
        else:
            items = cart.products
        in_cart = False
        for item in items:
            if item.product_id == product_id:
                count = item.count + quantity
                position_price = item.position_price + product.price * quantity
                product_query = (
                    update(CartItem)
                    .where(CartItem.id == product_id)
                    .values({"count": count, "position_price": position_price})
                )
                await self.db_session.execute(product_query)
                in_cart = True
                break
        if not in_cart:
            new_product = CartItem(
                product_id=product_id,
                cart_id=cart.id,
                count=quantity,
                position_price=quantity * product.price
            )
            self.db_session.add(new_product)
            await self.db_session.flush()
        products_count = cart.products_count + quantity
        total_price = cart.total_price + product.price * quantity
        cart_query = (
            update(Cart)
            .where(Cart.id == cart.id)
            .values({"products_count": products_count, "total_price": total_price})
        )
        await self.db_session.execute(cart_query)

    async def remove_product_from_cart(self, cart: Cart, product_id: int, quantity: int) -> None:
        product_query = select(Product).where(Product.id == product_id)
        product_row = await self.db_session.execute(product_query)
        product = product_row.fetchone()[0]
        if cart.products_count == 0:
            items = []
        else:
            items = cart.products
        in_cart = False
        for item in items:
            if item.product_id == product_id:
                if item.count > quantity:
                    count = item.count - quantity
                    position_price = item.position_price - product.price * quantity
                    product_query = (
                        update(CartItem)
                        .where(CartItem.product_id == product_id)
                        .values({"count": count, "position_price": position_price})
                    )
                else:
                    quantity = item.count
                    product_query = (
                        delete(CartItem)
                        .where(CartItem.product_id == product_id)
                    )
                await self.db_session.execute(product_query)
                in_cart = True
                break
        if not in_cart:
            raise HTTPException(status_code=404, detail="Товара не было в корзине")
        products_count = cart.products_count - quantity
        total_price = cart.total_price - product.price * quantity
        cart_query = (
            update(Cart)
            .where(Cart.id == cart.id)
            .values({"products_count": products_count, "total_price": total_price})
        )
        await self.db_session.execute(cart_query)

    async def get_cart_list(self, user_id: int) -> Cart | dict:
        cart_query = (
            select(Cart)
            .where(and_(
                Cart.user_id == user_id,
                Cart.payment_status == PaymentStatus.NOT_PAID
            ))
            .options(
                selectinload(Cart.products)
                .options(
                    joinedload(CartItem.product, innerjoin=True),
                )
            )
        )
        cart = await self.db_session.execute(cart_query)
        cart = cart.fetchone()
        if cart:
            return cart[0]
        return {
            "user_id": user_id,
            "total_price": 0,
            "payment_status": PaymentStatus.NOT_PAID,
            "products_count": 0,
            "products": []
        }
