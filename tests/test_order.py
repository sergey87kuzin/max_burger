import json

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from db_models import Order, User, OrderItem
from global_constants import PaymentType
from settings import TEST_PASSWORD


async def test_order_create(client, create_user_cart, async_session_test):
    cart = await create_user_cart(
        category_name="cart_category",
        product_name="cart product",
        username="cart_user@admin.ru"
    )
    access_data = {"username": "cart_user@admin.ru", "password": TEST_PASSWORD}
    tokens = client.post("api/users/token", data=access_data).json()
    token = tokens.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    data_dict = {
        "user_id": cart.user_id,
        "city": "some_city",
        "street": "some_street",
        "house_number": "some_house_number",
        "apartment": "123",
        "payment_type": PaymentType.CASH,
    }
    response = client.post(
        '/api/orders/create/',
        content=json.dumps(data_dict),
        headers=headers
    )
    created_order = response.json()

    assert response.status_code == 200

    async with async_session_test() as session:
        query = (
            select(Order)
            .join_from(Order, User)
            .options(
                selectinload(Order.products)
                .options(joinedload(OrderItem.product))
            )
            .options(
                joinedload(Order.user)
                .load_only(User.username)
            )
            .where(User.username == "cart_user@admin.ru")
        )
        orders = await session.execute(query)
        orders = list(orders.scalars())
    assert created_order in orders
