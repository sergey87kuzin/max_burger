import json

from global_constants import PaymentType
from settings import TEST_PASSWORD


async def test_order_create(client, create_user_cart):
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

    assert response.status_code == 200
