from fastapi import Header, HTTPException, Security, status
from app.core.config import settings


async def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
