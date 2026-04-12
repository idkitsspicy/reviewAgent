from fastapi import APIRouter, Query
from app.auth.oauth import exchange_code_for_token

router = APIRouter()

@router.get("/callback")
def oauth_callback(code: str = Query(...)):
    tokens = exchange_code_for_token(code)
    
    # store in DB (IMPORTANT)
    return {"message": "Connected successfully", "tokens": tokens}