import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from .. import models
from ..database import SessionLocal, engine
from ..main import app


@pytest.fixture
def db():
    db: Session = SessionLocal()
    yield db
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session):
    with TestClient(app) as client:
        yield client
