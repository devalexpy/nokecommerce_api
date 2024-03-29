from fastapi import APIRouter, Body, HTTPException, status, Depends
from security import get_client, verify_password, hash_password
from schemas.clients import ClientUpdate, ClientOut, ClientUpdatePassword
from db.clients_queries import get_client_by_id, update_client_data
from prisma.errors import PrismaError

router = APIRouter(
    prefix="/client",
    tags=["client"]
)


@router.put(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ClientOut,
)
async def update_client(client=Depends(get_client), client_data: ClientUpdate = Body(...)):

    client_data_update = client_data.dict(exclude_unset=True)

    if len(client_data_update) == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update",
        )

    if not verify_password(client_data_update["password"], client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    client_data_update.pop("password")
    client_updated = await update_client_data(client.id, client_data_update)
    if isinstance(client_updated, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(client_updated),
        )
    return client_updated


@router.put(
    path="/password",
)
async def update_client_password(client=Depends(get_client), client_data: ClientUpdatePassword = Body(...)):
    client_data_update = client_data.dict(exclude_unset=True)
    if len(client_data_update) == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update",
        )

    if not verify_password(client_data_update["password"], client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    client_data_update.pop("password")
    client_data_update["password"] = hash_password(
        client_data_update["new_password"])
    client_data_update.pop("new_password")
    client_updated = await update_client_data(client, client_data_update)
    if isinstance(client_updated, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(client_updated),
        )
    return {"detail": "Password updated"}
