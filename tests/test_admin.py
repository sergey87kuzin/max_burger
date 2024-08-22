import json

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


async def test_admin_users(client, get_user_from_database):
    response = client.post("api/admin/users/", data=json.dumps(user_data))
    assert response.status_code == 200

    user = await get_user_from_database("johndoe@gmail.com")
    assert user.first_name == "John", "Неверно передаются параметры пользователя при создании админом"
