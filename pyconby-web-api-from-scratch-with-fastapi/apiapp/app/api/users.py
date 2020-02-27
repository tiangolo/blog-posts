from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, models, schemas

router = APIRouter()


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read users.

    Doesn't require authentication.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Read the user data for the currently authenticated user.
    """
    return current_user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    """
    Read the data for a specific user.

    Doesn't require authentication.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/users/",
    response_model=schemas.User,
    dependencies=[Depends(deps.get_current_superuser)],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new user. Ony accessible by the superuser.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
