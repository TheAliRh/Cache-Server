from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.jwt import decode_access_token


oAuth2Scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")


async def get_current_user(token: str = Depends(oAuth2Scheme)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!."
        )
    return payload["sub"]
