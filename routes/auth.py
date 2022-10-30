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
    # response_model=ClientOut | AdminOut
)
async def login(client_data: OAuth2PasswordRequestForm = Depends(), admin: Optional[bool] = Query(default=False)):

    if admin:
        login_data = await get_admin_by_email(client_data.username)
        detail = "Admin not found"
    else:
        login_data = await get_client_by_email(client_data.username)
        detail = "Client not found"
    if login_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    if not verify_password(client_data.password, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = create_access_token(
        data={"sub": login_data.id}
    )
    login_data_dict = {key: value for key, value in login_data.dict(
    ).items() if key not in ["id", "password"]}
    login_data_dict.update(
        {"access_token": access_token, "token_type": "bearer"})
    return login_data_dict
