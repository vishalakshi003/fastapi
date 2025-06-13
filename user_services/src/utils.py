from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import timedelta,timezone,datetime
import jwt
from src.core.config import Config
from fastapi.security import OAuth2PasswordBearer
password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def generate_access_token(data:dict,expiry_time:timedelta=timedelta(days=1))->str:
    token = jwt.encode(payload={
        **data,
        'exp':datetime.now(timezone.utc) +expiry_time
    },algorithm=Config.JWT_ALGORITHM,key=Config.JWT_SECRET)
    return token

def jwt_decode_payload(token: str) -> dict:
    return jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM)
#httpbearer
security=HTTPBearer()
def fetch_current_user(tokens: HTTPAuthorizationCredentials = Security(security)) -> dict:
    payload = jwt_decode_payload(tokens.credentials)
    # user_id = payload.get("id")
    # name = payload.get("email")
    return payload
#oauth

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/users/api/oauth/login")