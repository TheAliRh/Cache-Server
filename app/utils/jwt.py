from jose import jwt, JWTError

from datetime import datetime, timedelta

from app.config import settings


# Create token
def create_access_token(data: dict):
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    return jwt.encode(toEncode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


# Decode token
def decode_access_token(token: str):
    try:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None
