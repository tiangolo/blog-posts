from fastapi import HTTPException


def get_query_token(token: str):
    if not token == "portalgun":
        raise HTTPException(400, detail="Invalid query token")
