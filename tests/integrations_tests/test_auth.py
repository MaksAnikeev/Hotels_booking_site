import pytest
from httpx import AsyncClient

from src.services.auth import AuthService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    decoder_token = AuthService().get_data_from_hash(jwt_token)
    assert decoder_token
    assert decoder_token["user_id"] == data["user_id"]


@pytest.mark.parametrize(
    "email, first_name, last_name, password_reg, password_log, status_code_add, status_code_login",
    [
        ("max@new.ru", "Maks", "Super", "1234", "1234", 200, 200),
        ("cat@pes.ru", "Maks", "Super", "1234", "1234", 409, 0),
        ("fgahsfsj", "Maks", "Super", "1234", "1234", 422, 422),
        ("new@new.ru", "New", "New", "1234", "wrong", 200, 401),
    ],
    ids=[
        "success create, loging and use",
        "wrong create exist email",
        "wrong create incorrect email",
        "wrong loging incorrect password",
    ],
)
async def test_auth_flow(
    email,
    first_name,
    last_name,
    password_reg,
    password_log,
    status_code_add,
    status_code_login,
    check_test,
    ac: AsyncClient,
):
    new_user_info = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password_reg,
    }
    # registration
    response_reg = await ac.post("/user/add", json=new_user_info)
    assert response_reg.status_code == status_code_add
    resp = response_reg.json()
    if response_reg.status_code == 200:
        assert resp["status"] == "OK"
        assert resp["user_info"]["email"] == new_user_info["email"]
        assert (
            resp["description"]
            == f"Новый пользователь {new_user_info['first_name']} успешно добавлен"
        )
    elif response_reg.status_code == 409:
        assert resp["detail"] == "Пользователь с таким email уже существует"
        return

    # login
    assert "access_token" not in ac.cookies
    response_log = await ac.post(
        "/user/login", json={"email": new_user_info["email"], "password": password_log}
    )
    assert response_log.status_code == status_code_login
    resp = response_log.json()
    if response_log.status_code == 200:
        assert resp["status"] == "OK"
        assert resp["description"] == "JWT token успешно создан"
        assert ac.cookies["access_token"] == resp["access_token"]
    elif response_log.status_code == 401:
        assert resp["detail"] == "Неверно указан пароль"
        return
    else:
        return

    # who are me
    response_me = await ac.get("/user/me")
    assert response_me.status_code == 200
    resp = response_me.json()
    assert resp["data"]["first_name"] == new_user_info["first_name"]
    assert "password" not in resp["data"]
    assert "hashed_password" not in resp["data"]

    # logout
    response_logout = await ac.post("/user/logout")
    assert response_logout.status_code == 200

    # Unauthorized
    response_me = await ac.get("/user/me")
    assert response_me.status_code == 401
