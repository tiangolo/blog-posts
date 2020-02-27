from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from . import utils


def test_create_item(client: TestClient, db: Session):
    token = utils.get_superuser_access_token(db)
    headers = utils.get_token_headers(token)
    user = utils.create_test_user(db)
    item_data = {"title": "In Test Item", "description": "In test description"}
    response = client.post(f"/users/{user.id}/items/", json=item_data, headers=headers)
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["owner_id"] == user.id


def test_read_item(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    item = utils.create_test_item(db=db, user=user)
    response = client.get("/items/")
    data = response.json()
    assert data
    is_in_response = False
    for it in data:
        if item.id == it["id"] and item.owner_id == it["owner_id"]:
            is_in_response = True
    assert is_in_response


def test_create_item_self_user(client: TestClient, db: Session):
    user = utils.create_test_user(db)
    token = utils.get_user_access_token(user)
    token_headers = utils.get_token_headers(token)
    item_data = {"title": "Own Item", "description": "Own item description"}
    response = client.post("/items/", json=item_data, headers=token_headers)
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["owner_id"] == user.id
