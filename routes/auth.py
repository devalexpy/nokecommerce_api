from fastapi import (
    APIRouter, Body, HTTPException,
    status
)
from prisma.errors import PrismaError
from schemas.clients import ClientSingUp, clientLogin
from db.clients_queries import create_client, get_client
from security import hash_password, create_access_token, verify_password


auth = APIRouter()


@auth.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
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


@auth.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    tags=["auth"],
)
async def login(client_data: clientLogin = Body(...)):
    client = await get_client(client_data.email)
    if isinstance(client, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(client),
        )
    if not verify_password(client_data.password, client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = create_access_token(
        data={"sub": client.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
