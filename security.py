from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="auth/login/admin")


def hash_password(password: str):
    return pass_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=float(config("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config(
        'SECRET_KEY'), algorithm=config('ALGORITHM'))
    return encoded_jwt


async def get_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config(
            'SECRET_KEY'), algorithms=[config('ALGORITHM')])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
            credentials_exception.detail = "Token expired"
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
