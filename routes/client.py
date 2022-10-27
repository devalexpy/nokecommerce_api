from fastapi import APIRouter, Body, HTTPException, status, Depends
from security import get_user_id
from schemas.clients import clientOut
from prisma.errors import PrismaError
from db.clients_queries import get_client_by_id

router = APIRouter(
    prefix="/client",
    tags=["client"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=clientOut,
)
async def get_client(id=Depends(get_user_id)):
    client = await get_client_by_id(id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return client
