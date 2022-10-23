from fastapi import (
    APIRouter, Body, HTTPException,
    status
)
from schemas.clients import ClientOut, ClientSingUp
from db.clients_queries import create_client
from passlib.context import CryptContext

auth = APIRouter()

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth.post(
    path="/signup",
    response_model=ClientOut,
    tags=["auth"],
)
async def signup(client_data: ClientSingUp = Body(...)):
    client_data.password = pass_context.hash(client_data.password)
    client = await create_client(client_data.dict())
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return dict(client)  # type: ignore
