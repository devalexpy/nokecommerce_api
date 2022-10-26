from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from decouple import config

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pass_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config(
        'SECRET_KEY'), algorithm=config('ALGORITHM'))
    return encoded_jwt
