from datetime import datetime, timedelta
from passlib.context import CryptContext
from config import settings, VERIFICATION_TOKEN_EXPIRE_HOURS, ALGORITHM
from fastapi_cache import FastAPICache
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_redis():
    return FastAPICache.get_backend()

def create_verification_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
