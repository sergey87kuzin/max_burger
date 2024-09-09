import json

from settings import TEST_PASSWORD


async def test_add_cart(client, create_admin, create_product):
    user = await create_admin("add_to_cart_user@admin.ru", TEST_PASSWORD)
    product = await create_product("cart_add_category", "cart_add_product")
    add_cart_data = {"user_id": user.id, "product_id": product.id, "quantity": 1}
    response = client.post("/api/cart/add/", content=json.dumps(add_cart_data))
    assert response.status_code == 200
