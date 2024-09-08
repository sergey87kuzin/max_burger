import json

import pytest
from sqlalchemy import select

from db_models import Order
from global_constants import PaymentType, DeliveryType
from settings import TEST_PASSWORD


@pytest.mark.parametrize(
    "category_name,product_name,username,payment_type,delivery_type",
    (
        ("cart_category_1", "cart product_1", "cart_user_1@admin.ru", PaymentType.CASH, DeliveryType.IN_REST),
        ("cart_category_2", "cart product_2", "cart_user_2@admin.ru", PaymentType.CASH, DeliveryType.COURIER),
        ("cart_category_3", "cart product_3", "cart_user_3@admin.ru", PaymentType.CARD_COURIER, DeliveryType.IN_REST),
        ("cart_category_4", "cart product_4", "cart_user_4@admin.ru", PaymentType.CARD_COURIER, DeliveryType.COURIER),
    )
)
async def test_order_create(
        category_name,
        product_name,
        username,
        payment_type,
        delivery_type,
        client,
        create_user_cart,
        async_session_test
):
    cart = await create_user_cart(
        category_name=category_name,
        product_name=product_name,
        username=username
    )
    access_data = {"username": username, "password": TEST_PASSWORD}
    tokens = client.post("api/users/token", data=access_data).json()
    token = tokens.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    data_dict = {
        "user_id": cart.user_id,
        "city": "some_city",
        "street": "some_street",
        "house_number": "some_house_number",
        "apartment": "123",
        "payment_type": payment_type,
        "delivery_type": delivery_type,
    }
    response = client.post(
        '/api/orders/create/',
        content=json.dumps(data_dict),
        headers=headers
    )
    created_order = response.json()

    assert response.status_code == 200

    async with async_session_test() as session:
        query = select(Order).where(Order.id == created_order['order_id'])
        order_from_db = await session.execute(query)
        order_from_db = order_from_db.scalar()
    for key, value in data_dict.items():
        assert getattr(order_from_db, key) == value
