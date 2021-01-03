from fastapi import APIRouter, Depends
from .dependencies import get_query_token

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(get_query_token)]
)


@router.get("/users/")
def read_users():
    return ["rick", "morty"]
