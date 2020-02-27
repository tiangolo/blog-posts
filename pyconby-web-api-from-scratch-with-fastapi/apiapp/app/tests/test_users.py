from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from .. import security
from . import utils


def test_read_users(client: TestClient, db: Session):
    utils.create_test_user(db)
    response = client.get("/users/")
    data = response.json()
    assert data
    assert len(data) > 0


def test_create_user(client: TestClient, db: Session):
    token = utils.get_superuser_access_token(db)
    token_headers = utils.get_token_headers(token)
    response = client.post(
        "/users/",
        json={"email": "john@example.com", "password": "johnpass"},
        headers=token_headers,
    )
    data = response.json()
    assert data["email"] == "john@example.com"
    assert "password" not in data


def test_read_user(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    response = client.get(f"/users/{user.id}")
    data = response.json()
    assert data["email"] == user.email


def test_read_user_me(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    token = utils.get_user_access_token(user)
    token_headers = utils.get_token_headers(token)
    response = client.get("/users/me", headers=token_headers)
    data = response.json()
    assert data["email"] == user.email


def test_authenticate_user(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    response = client.post(
        "/login/access-token",
        data={"username": "test@example.com", "password": "examplesecret"},
    )
    data = response.json()
    assert "access_token" in data

    token = data["access_token"]
    token_headers = utils.get_token_headers(token)
    response = client.get("/users/me", headers=token_headers)
    data = response.json()
    assert data["email"] == user.email


def test_authenticate_user_incorrect_password(client: TestClient, db: Session):
    utils.create_test_user(db)
    response = client.post(
        "/login/access-token",
        data={"username": "test@example.com", "password": "incorrectpassword"},
    )
    assert response.status_code == 400


def test_authenticate_user_incorrect_email(client: TestClient, db: Session):
    utils.create_test_user(db)
    response = client.post(
        "/login/access-token",
        data={"username": "incorrectemail@example.com", "password": "examplesecret"},
    )
    assert response.status_code == 400


def test_create_user_not_superuser(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    token = utils.get_user_access_token(user)
    token_headers = utils.get_token_headers(token)
    response = client.post(
        "/users/",
        json={"email": "john@example.com", "password": "johnpass"},
        headers=token_headers,
    )
    assert response.status_code == 403


def test_read_user_not_existent(client: TestClient, db: Session):
    utils.create_test_user(db)
    response = client.get("/users/42")
    assert response.status_code == 404


def test_read_user_me_invalid_token(client: TestClient):
    token = "invalidtoken"
    token_headers = utils.get_token_headers(token)
    response = client.get("/users/me", headers=token_headers)
    assert response.status_code == 403


def test_read_user_me_valid_token_inexistent_user(client: TestClient):
    token = security.create_access_token(subject=42)
    token_headers = utils.get_token_headers(token)
    response = client.get("/users/me", headers=token_headers)
    assert response.status_code == 404


def test_create_user_same_email(client: TestClient, db: Session):
    token = utils.get_superuser_access_token(db)
    token_headers = utils.get_token_headers(token)
    user_data = {"email": "john@example.com", "password": "johnpass"}
    response = client.post("/users/", json=user_data, headers=token_headers)
    assert response.status_code == 200

    response = client.post("/users/", json=user_data, headers=token_headers)
    assert response.status_code == 400
