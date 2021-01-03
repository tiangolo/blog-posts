from fastapi import FastAPI, Depends
from .dependencies import get_query_token

app = FastAPI(
    dependencies=[Depends(get_query_token)]
)

@app.get("/")
def main():
    return {"message": "Hello World"}
