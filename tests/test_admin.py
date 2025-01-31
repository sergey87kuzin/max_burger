import json
from http import HTTPStatus

import pytest
from sqlalchemy import select

from db_models import User, Category, Product
from settings import TEST_PASSWORD

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


class TestAdmin:
    @pytest.fixture(autouse=True)
    async def setup(self, client, create_admin, async_session_test):
        await create_admin("GreyTres@admin.ru", TEST_PASSWORD)
        access_data = {"username": "GreyTres@admin.ru", "password": TEST_PASSWORD}
        tokens = client.post("api/users/token", data=access_data).json()
        token = tokens.get("access_token")
        self.headers = {"Authorization": f"Bearer {token}"}

        new_category = Category(
            name="test_category",
            is_active=True,
        )
        async with async_session_test() as session:
            session.add(new_category)
            await session.commit()
        self.category_id = new_category.id

    @pytest.mark.parametrize(
        "url,model,data_dict,update_data_dict", [
            ("categories", Category, category_data, category_update_data),
            ("products", Product, product_data, product_update_data),
            ("users", User, user_data, user_update_data),
        ]
    )
    async def test_admin_objects(
            self,
            url,
            model,
            data_dict,
            update_data_dict,
            client,
            async_session_test,
            create_admin
    ):
        if url == "products":
            data_dict["category_id"] = self.category_id  # new_category.id

        response = client.post(f"api/admin/{url}/", content=json.dumps(data_dict), headers=self.headers)
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

        update_response = client.post(
            f"api/admin/{url}/{object_from_db_id}/",
            content=json.dumps(update_data_dict),
            headers=self.headers,
        )
        assert update_response.status_code == 200

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

        updated_data = update_response.json()

        single_response = client.get(url=f"api/admin/{url}/{object_from_db_id}/", headers=self.headers)
        assert single_response.status_code == HTTPStatus.OK, "Неверный статус запроса к деталке объекта"
        assert single_response.json() == updated_data, "Некорректные данные в возрате деталки или изменения"

        list_response = client.get(url=f"api/admin/{url}/list/", headers=self.headers)
        assert list_response.status_code == HTTPStatus.OK, "Неверный статус запроса к списку объектов"
        resp_data = list_response.json()
        assert "objects_count" in resp_data and "objects" in resp_data, "Не прикручена пагинация"
        assert updated_data in resp_data.get("objects"), "Объекта нет в списке либо он там отображен некорректно"

        delete_response = client.delete(url=f"api/admin/{url}/{object_from_db_id}/", headers=self.headers)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        single_response = client.get(url=f"api/admin/{url}/{object_from_db_id}/", headers=self.headers)
        assert single_response.status_code == HTTPStatus.NOT_FOUND, "Неверный статус запроса к деталке объекта"


    @pytest.mark.parametrize(
        "url,model,data_dict",
        [
            ("categories", Category, category_data),
            ("products", Product, product_data),
            ("users", User, user_data),
        ]
    )
    async def test_admin_pagination(self, url, model, data_dict, client, async_session_test):
        if url == "products":
            new_category = Category(
                name="test_category",
                is_active=True,
            )
            async with async_session_test() as session:
                session.add(new_category)
                await session.commit()
            data_dict["category_id"] = new_category.id
        if url == "users":
            key = "username"
        else:
            key = "name"
        async with async_session_test() as session:
            for index in range(25):
                data_dict[key] = f"{model.__name__}_{index}@some.url"
                new_object = model(**data_dict)
                session.add(new_object)
            await session.commit()
        list_response = client.get(url=f"api/admin/{url}/list/?page=2&size=10", headers=self.headers)
        assert list_response.status_code == HTTPStatus.OK, "Неверный статус запроса при наличии пагинации"
        resp_data = list_response.json()
        assert resp_data.get("objects_count") > 2
        assert len(resp_data.get("objects")) == 10
