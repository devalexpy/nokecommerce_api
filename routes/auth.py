from fastapi import (
    APIRouter, Body, HTTPException,
    status, Depends
)
from fastapi.security import OAuth2PasswordRequestForm
from prisma.errors import PrismaError
from schemas.clients import ClientSingUp
from db.clients_queries import create_client, get_client_by_email
from security import hash_password, create_access_token, verify_password


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
)
async def login(client_data: OAuth2PasswordRequestForm = Depends()):
    login_data = await get_client_by_email(client_data.username)
    if login_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    if not verify_password(client_data.password, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token = create_access_token(
        data={"sub": login_data.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
