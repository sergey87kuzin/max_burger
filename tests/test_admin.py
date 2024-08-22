import json

import pytest
from sqlalchemy import select

from db_models import User, Category, Product

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe@gmail.com",
    "phone": "+79111111111",
    "password": "123456Nn",
    "is_active": True,
    "is_staff": True,
    "is_admin": True,
}

category_data = {
    "name": "new_category",
    # "cover": "cover.png",
    "is_active": True,
}

product_data = {
    "name": "new_product",
    "is_combo_product": True,
    "is_active": True,
    "price": 10,
    "description": "description",
    # "image": "cover.png",
}


@pytest.mark.parametrize(
    "url,model,data_dict", [
        ("users", User, user_data),
        ("categories", Category, category_data),
        ("products", Product, product_data),
    ]
)
async def test_admin_objects_creation(url, model, data_dict, client, async_session_test):

    if url == "products":
        new_category = Category(
            name="test_category",
            is_active=True,
        )
        async with async_session_test() as session:
            session.add(new_category)
            await session.commit()
        data_dict["category_id"] = new_category.id

    response = client.post(f"api/admin/{url}/", data=json.dumps(data_dict))
    assert response.status_code == 200

    async with async_session_test() as session:
        results = await session.execute(select(model).where(model.id == response.json().get("id")))
        if results:
            result = results.first()[0]
        else:
            raise AssertionError("Object not found")
    for key, value in data_dict.items():
        if key != "password":
            assert getattr(result, key) == value
