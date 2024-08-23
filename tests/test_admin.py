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

user_update_data = {
    "first_name": "Linda",
    "last_name": "Thompson",
}
category_update_data = {
    "name": "accessories",
}
product_update_data = {
    "name": "super accessories",
}


@pytest.mark.parametrize(
    "url,model,data_dict,update_data_dict", [
        ("users", User, user_data, user_update_data),
        ("categories", Category, category_data, category_update_data),
        ("products", Product, product_data, product_update_data),
    ]
)
async def test_admin_objects(url, model, data_dict, update_data_dict, client, async_session_test):

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
    object_from_db_id = response.json()["id"]

    async with async_session_test() as session:
        results = await session.execute(select(model).where(model.id == object_from_db_id))
        if results:
            result = results.first()[0]
        else:
            raise AssertionError("Object not found")
    for key, value in data_dict.items():
        if key == "password":
            continue
        assert getattr(result, key) == value, "Неверное сохранение объекта в бд"

    response = client.post(f"api/admin/{url}/{object_from_db_id}/", data=json.dumps(update_data_dict))
    assert response.status_code == 200

    async with async_session_test() as session:
        results = await session.execute(select(model).where(model.id == object_from_db_id))
        if results:
            result = results.first()[0]
        else:
            raise AssertionError("Object not found")

    for key, value in update_data_dict.items():
        assert getattr(result, key) == value, "Неверное изменение объекта в бд"

    for key, value in data_dict.items():
        if key == "password":
            continue
        if key in update_data_dict:
            continue
        assert getattr(result, key) == value, "Изменены лишние поля объекта в бд"
