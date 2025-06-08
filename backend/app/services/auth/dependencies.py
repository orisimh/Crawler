from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from app.services.auth.jwt_handler import decode_access_token
from fastapi import Request
from app.core.config import get_settings

settings = get_settings()

async def get_current_user(token: Optional[str] = Header(None)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return payload

def extract_final_path(request: Request) -> str:
    path = request.url.path
    if f"/{settings.v}/" in path:
        return path.split(f"/{settings.v}/")[-1].split("/")[0]
    return ""