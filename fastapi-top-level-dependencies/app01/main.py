from fastapi import FastAPI, Depends
from . import users
from .dependencies import get_query_token

app = FastAPI()

app.include_router(
    users.router,
    tags=["users"],
    dependencies=[Depends(get_query_token)]
)


@app.get("/")
def main():
    return {"message": "Hello World"}

