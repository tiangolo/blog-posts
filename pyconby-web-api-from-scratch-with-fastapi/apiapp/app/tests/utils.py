from sqlalchemy.orm import Session

from .. import crud, models, schemas, security
from ..settings import settings


def get_superuser_access_token(db: Session):
    superuser = crud.get_user_by_email(db, email=settings.super_user_email)
    return get_user_access_token(superuser)


def get_token_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def get_user_access_token(user: models.User):
    return security.create_access_token(subject=user.id)


def create_test_user(db: Session):
    user_in = schemas.UserCreate(email="test@example.com", password="examplesecret")
    return crud.create_user(db, user=user_in)


def create_test_item(db: Session, user: models.User):
    item_in = schemas.ItemCreate(
        title="Example Item", description="Example description"
    )
    return crud.create_user_item(db, item=item_in, user_id=user.id)
