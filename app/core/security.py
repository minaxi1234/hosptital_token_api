from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError

from app.core.config import settings


ALGORITHM = "HS256"




def create_access_token(data: Dict, expires_minutes: Optional[int] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict, expires_minutes: Optional[int] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise


# def verify_token(token: str):
#     """
#     Returns payload if token is valid, else None.
#     routers will use this for role protection later.
#     """
#     payload = decode_token(token)
#     return payload

