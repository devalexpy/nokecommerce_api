from fastapi import (
    APIRouter, Body, HTTPException,
    status, Depends, Query
)
from fastapi.security import OAuth2PasswordRequestForm
from prisma.errors import PrismaError
from schemas.clients import ClientSingUp, ClientOut
from schemas.admins import AdminOut
from db.clients_queries import create_client, get_client_by_email
from db.admin_queries import get_admin_by_email
from security import hash_password, create_access_token, verify_password
from typing import Optional


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
)
async def signup(client_data: ClientSingUp = Body(...)):
    client_data.password = hash_password(client_data.password)
    client = await create_client(client_data.dict())
    if isinstance(client, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(client),
        )
    return {"message": "Client created successfully"}


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=ClientOut
)
async def login(client_data: OAuth2PasswordRequestForm = Depends()):
    client = await get_client_by_email(client_data.username)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    if not verify_password(client_data.password, client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = create_access_token(
        data={"sub": client.id}
    )
    login_data_dict = {key: value for key, value in client.dict(
    ).items() if key not in ["id", "password"]}
    login_data_dict.update(
        {"access_token": access_token, "token_type": "bearer"})
    return login_data_dict


@router.post(
    path="/login/admin",
    status_code=status.HTTP_200_OK,
    response_model=AdminOut
)
async def login_admin(admin_data: OAuth2PasswordRequestForm = Depends()):
    admin = await get_admin_by_email(admin_data.username)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    if not verify_password(admin_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = create_access_token(
        data={"sub": admin.id}
    )
    login_data_dict = {key: value for key, value in admin.dict(
    ).items() if key not in ["id", "password"]}
    login_data_dict.update(
        {"access_token": access_token, "token_type": "bearer"})
    return login_data_dict
