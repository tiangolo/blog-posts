from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, deps, models, schemas

router = APIRouter()


@router.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(deps.get_current_superuser)],
)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(deps.get_db)
):
    """
    Create an item for a specific user.

    Only allowed to the super user.
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.post("/items/", response_model=schemas.Item)
def create_item_for_current_user(
    item: schemas.ItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create an item.

    Requires authentication and the item will be assigned to the current user.
    """
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the items. Doesn't need authentication.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
