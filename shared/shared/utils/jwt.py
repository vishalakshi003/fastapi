# shared/shared/utils/jwt.py

import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from shared.core.config import config
from fastapi import Security, HTTPException, status

def generate_access_token(data: Dict, expiry_time: timedelta = timedelta(days=config.TOKEN_EXPIRE_DAYS)) -> str:
    print('Token encode called')
    """Generates a JWT access token with an expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expiry_time
    print('algorithm',config.JWT_ALGORITHM,config.JWT_SECRET)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def jwt_decode_payload(token: str) -> dict:
    print('Token decode called')
    """Decodes a JWT token and returns the payload. Raises HTTP exceptions if invalid or expired."""
    try:
        print('algorithm',config.JWT_ALGORITHM,config.JWT_SECRET)
        return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
